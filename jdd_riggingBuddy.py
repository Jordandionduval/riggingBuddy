#-----------------------------Tested for Maya 2022+-----------------------------#
#
#             jdd_riggingBuddy.py 
#             v0.0.0, last modified 15/08/22
# 
# MIT License
# Copyright (c) 2020 Jordan Dion-Duval
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
#----------------------------------INSTALLATION---------------------------------#
# 1. Copy the "jdd_riggingBuddy.py" to your Maya scripts directory:
#     > MyDocuments\Maya\scripts\
# 2. Then, within maya, use the following text as a python script to run the tool:
#    (without the apostrophes)
'''
import jdd_riggingBuddy as RB
RB.UI()
'''
# 3.(Optional) Alternatively, the text can be saved in the custom shelf using
# maya's script editor. This makes the script a small button in your current shelf
# so it can easily be accessed later.
#--------------------------------------------------------------------------------#
from imp import source_from_cache
import maya.cmds as cmds

class buddyRigg_Window(object):
        
    #----------------------------------------------constructor----------------------------------------------#
    def __init__(self):
        
        self.window = "buddyRigg_Window"
        self.title = "Rigging Buddy"
        windowW = 400
        windowH = 500
        self.size = (windowW, windowH)
            
        #focus if window open #WIP
        #if cmds.window(self.window, exists = True):
        #    cmds.showWindow()
        if cmds.window(self.window, exists = True):
            cmds.deleteUI(self.window, window=True)
            print('\nRestarting instance of Rigging Buddy...\n')

        else:
            print('\nLaunching a new instance of Rigging Buddy...\n')
    
        #create new window
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        
        #----------------------------------------------UI Layout----------------------------------------------#
        #-----------------------------------UI Definition-----------------------------------#
        form = cmds.formLayout()
        tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        

        cmds.formLayout(form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)))
        #-----------------------------------UI Tab Build-----------------------------------#
        buildTab = cmds.columnLayout(cw=windowW)
        cmds.frameLayout(label='Controllers', collapsable = True, collapse = False, lw = windowW, mw = 5)
        cmds.rowColumnLayout(nc=3, cw = [(1, 100), (2, 180), (3, 80)],
                                   co = [(1,'left', 4), (2,'both', 4), (3,'right', 4)])
        cmds.text(l='Controller', al = 'left')
        self.ctrlNameInput = cmds.textField(tx='CTRL_', cc = self.updateCtrlNameInput)
        self.constraintCheck = cmds.checkBox(l='Constraint', al = 'left', v = True, cc = self.updateConstraintCheck)
        cmds.text(l='Offset', al = 'left')
        self.offsetNameInput = cmds.textField(tx='Offset_', cc = self.updateOffsetNameInput)
        cmds.setParent('..')

        cmds.separator(style='none', h=5)

        cmds.rowColumnLayout(nc=3, cw = [(1, 100), (2, 60), (3, 160)],
                                   co = [(1,'left', 4), (2,'both', 4), (3,'right', 4)])
        cmds.text(l='Radius Multiplier')
        self.radiusFloat = cmds.floatField(v=1, min=0, cc = self.updateRadiusFloat)
        self.radiusCheck = cmds.checkBox(l='Use custom scale by name', al = 'left', v = True, cc = self.updateRadiusCheck)
        cmds.setParent('..')

        cmds.rowColumnLayout(nc=4, cw = [(1, 160), (2, 60), (3, 60), (4, 60)],
                                   co = [(1,'right', 4), (2,'right', 4), (3,'right', 4), (4,'right', 4)])
        cmds.text(l='Controller Orientation')
        self.orientAxisCollection = cmds.radioCollection()
        self.orientX = cmds.radioButton(l='x', cc = self.ctrlOrient)
        self.orientY = cmds.radioButton(l='y', cc = self.ctrlOrient)
        self.orientZ = cmds.radioButton(l='z', cc = self.ctrlOrient)
        cmds.setParent('..')
        
        cmds.radioCollection(self.orientAxisCollection, edit=True, sl=self.orientY)

        cmds.columnLayout()
        self.addCtrlButton = cmds.button(l = "Add controls", command = self.addCtrl, w=windowW)
        cmds.setParent('..')

        cmds.separator(style='none', w=windowW, h=5)

        cmds.setParent('..')
        
        cmds.frameLayout(label='Selection', collapsable = True, collapse = False, lw = windowW, mw = 5)
        uiSelect = [
                    "All",
                    "Selection",
                    "Hierarchy",
                    "Curves",
                    "Joints",
                    "Geometry"
                    ]

        cmds.rowColumnLayout(nc=5,  cw=[(1, 80), (2, 100), (3, 100), (4, 100)],
                                    co=[(1,'both', 2), (2,'both', 2), (3,'both', 2), (4,'both',2)])
        cmds.text(l='  Method', al = 'left')
        self.selectMethodCollection = cmds.radioCollection()
        self.selectMethod1 = cmds.radioButton(l=uiSelect[1], cc = self.selectionMethod, onc = self.selectionStatus)
        self.selectMethod2 = cmds.radioButton(l=uiSelect[2], cc = self.selectionMethod, onc = self.selectionStatus)
        self.selectMethod3 = cmds.radioButton(l=uiSelect[0], cc = self.selectionMethod, onc = self.selectionStatus)
        cmds.setParent('..')
        
        cmds.radioCollection(self.selectMethodCollection, edit=True, sl=self.selectMethod1)
        
        cmds.separator(style='none', h=8)
        
        cmds.rowColumnLayout(nc=5,  cw=[(1, 80), (2, 80), (3, 80), (4, 80), (5, 80)],
                                    co=[(1,'both', 2), (2,'both', 2), (3,'both', 2), (4,'both',2), (5,'both',2)])
        cmds.text(l='  Quick Select', al = 'left')
        self.selectHiButton = cmds.button(l = uiSelect[2], command = self.selectHi)
        self.selectCrvButton = cmds.button(l = uiSelect[3], command = self.selectCrv)
        self.selectJntButton = cmds.button(l = uiSelect[4], command = self.selectJnt)
        self.selectGeoButton = cmds.button(l = uiSelect[5], command = self.selectGeo)
        cmds.setParent('..')

        cmds.separator(style='none', w=windowW, h=5)

        cmds.setParent('..')

        cmds.setParent('..')
        #-----------------------------------UI Tab Pose-----------------------------------#
        poseTab = cmds.columnLayout(cw=windowW)
        cmds.rowColumnLayout(nc=2, cs = [(1, 0), (2, 50)], cw = [(1, 240), (2, 50)])
        #Source/Target Lists
        cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
        cmds.rowColumnLayout(nc=2)
         
        self.sourceList = cmds.textScrollList(allowMultiSelection=True, append=[])
        self.updateSourceList
        cmds.textScrollList(append=['other_R'])
        
        self.testButton = cmds.button(l = 'test', command = self.runTest)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        #-----------------------------------UI Tabulation-----------------------------------#
        cmds.tabLayout( tabs, edit=True, tabLabel=((buildTab, 'Build'), (poseTab, 'Pose')) )
        #display new window
        cmds.showWindow()
    #----------------------------------------------Functions----------------------------------------------#
    #-----------------------------------General-----------------------------------#
    def funcSort(self, func, x, y='notNested'):
        resList = func()
        sortedList = resList[x]
        if type(y) == int:
            res = sortedList[y]
        else:
            res = sortedList
        return res
    
    def zeroPad(self, num, pad):
        x = len(str(num))
        y = pad - x
        if pad < x:
            y = 0
        z = '0' * y + str(num)
        return z
    
    def bottomTop_2t(self, selectionList):
        trueNameList = []
        for i in selectionList:
            if cmds.listRelatives(i, f = True) == None:
                try:
                    parent = cmds.listRelatives(i, p = True, f = True)
                    fullPath = cmds.listRelatives(parent, f = True)
                    fullPath = fullPath[0].split('|')
                except TypeError:
                    fullPath = i
            else:
                fullPath = cmds.listRelatives(i, f = True)
                fullPath = fullPath[0].split('|')[:-1]
            
            depth = len(fullPath)
            trueNameList = trueNameList + [(i, depth)]
        
        # Sorting list by path depth: We don't want our renaming reference to be changed mid-operation,
        # as it would cause problems down the hierarchy when renaming other objects
        depthNameList = sorted(trueNameList, key=lambda tup: tup[1], reverse = 1)

        return depthNameList


    def quickAdd(self, quickName, isPrefix, separator='_'):
        operationCount = 0
        
        selectionList = self.funcSort(self.selectionMethod, 1)
        depthNameList = self.bottomTop_2t(selectionList) 

        for i in depthNameList:
            _object, _depth = i
            oldName = _object.split('|')[-1]
            if isPrefix == True:
                newName = quickName + separator + oldName
            else:
                newName = oldName + separator + quickName
            
            cmds.rename(_object, newName)
            operationCount += 1
        
        if operationCount > 0:
            print("Added " + quickName + " to " + str(operationCount) + " object(s).")
    
    def updateQuickUi(self, con1, con2):
        uiQuick = [
                    "Grp", 
                    "Ctrl", 
                    "Drv", 
                    "Jnt", 
                    "Geo", 
                    "L", 
                    "C", 
                    "R"
                    ]
        
        separator = '_'
        if con2 == True:
            makeSuffix = ''
            makePrefix = separator
        else:
            makeSuffix = separator
            makePrefix = ''

        if con1 == True:
            cmds.button(self.quickGrp, e = True, l = makeSuffix + uiQuick[0].upper() + makePrefix)
            cmds.button(self.quickCtrl, e = True, l = makeSuffix + uiQuick[1].upper() + makePrefix)
            cmds.button(self.quickDrv, e = True, l = makeSuffix + uiQuick[2].upper() + makePrefix)
            cmds.button(self.quickJnt, e = True, l = makeSuffix + uiQuick[3].upper() + makePrefix)
            cmds.button(self.quickGeo, e = True, l = makeSuffix + uiQuick[4].upper() + makePrefix)
            cmds.button(self.quickL, e = True, l = makeSuffix + uiQuick[5].upper() + makePrefix)
            cmds.button(self.quickC, e = True, l = makeSuffix + uiQuick[6].upper() + makePrefix)
            cmds.button(self.quickR, e = True, l = makeSuffix + uiQuick[7].upper() + makePrefix)
        else:
            cmds.button(self.quickGrp, e = True, l = makeSuffix + uiQuick[0] + makePrefix)
            cmds.button(self.quickCtrl, e = True, l = makeSuffix + uiQuick[1] + makePrefix)
            cmds.button(self.quickDrv, e = True, l = makeSuffix + uiQuick[2] + makePrefix)
            cmds.button(self.quickJnt, e = True, l = makeSuffix + uiQuick[3] + makePrefix)
            cmds.button(self.quickGeo, e = True, l = makeSuffix + uiQuick[4] + makePrefix)
            cmds.button(self.quickL, e = True, l = makeSuffix + uiQuick[5] + makePrefix)
            cmds.button(self.quickC, e = True, l = makeSuffix + uiQuick[6] + makePrefix)
            cmds.button(self.quickR, e = True, l = makeSuffix + uiQuick[7] + makePrefix)
    
    def fastReplace(self, target, replacement=''):
        operationCount = 0
        failureCount = 0
        failureList = []
        illegalCount = 0
        illegalList = []
        
        selectionList = self.funcSort(self.selectionMethod, 1)
        depthNameList = self.bottomTop_2t(selectionList) 

        for i in depthNameList:
            _object, _depth = i
            
            if self.setMatchCaseCheck() == False:
                l = len(target)
                oldName = _object.upper().split('|')[-1]
                try:
                    n = oldName.index(target.upper())

                    oldName = _object.split('|')[-1]
                    newName = oldName[:n] + replacement + oldName[(n+l):]
                except:
                    oldName = _object.split('|')[-1]
                    newName = oldName
            else:
                oldName = _object.split('|')[-1]
                newName = oldName.replace(target, replacement)
            
            if newName[0].isalpha() == False:
                if newName[0] != '_':
                    True
                else:
                    illegalCount += 1
                    illegalList += cmds.ls(_object, sn = True)
                    continue

            cmds.rename(_object, newName)
            if target not in oldName:
                if self.setMatchCaseCheck() == False and target.upper() in oldName.upper():
                    operationCount += 1
                else:
                    failureCount += 1
                    failureList += cmds.ls(_object, sn = True)
            else:
                operationCount += 1
        
        if operationCount > 0:
            if replacement == '':
                print("Removed \"" + target + "\" from " + str(operationCount) + " object(s)")
            else:
                print("Replaced \"" + target + "\" with \"" + replacement + "\" in " + str(operationCount) + " object(s)")
        if illegalCount > 0:
            print("# ValueError\n# Failed operations (" + str(illegalCount) + "): " + str(failureList))
            raise ValueError("Resulting object names would start with an illegal character")
        if failureCount > 0:
            if operationCount > 0:
                print("# Warning\n# Failed operations (" + str(failureCount) + "): " + str(failureList))
                raise Warning("Could not find search name from certain objects in current selection")
            else:
                print("# ValueError\n# Failed operations (" + str(failureCount) + "): " + str(failureList))
                raise ValueError("Could not find search name in current selection")
    
    def listSl(self):
        res = cmds.ls(sl=True)

        return res

    def listHi(self):
        cmds.select(hi=True)
        res = cmds.ls(sl=True, dag = True)
        cmds.undo()
        
        illegalObjects = cmds.ls(res, s = True)
        for i in illegalObjects:
            if i in res:
                res.remove(i)
        
        return res
    
    def listAll(self):
        res = cmds.ls(dag=True)
        illegalObjects = cmds.ls(ca=True)
        illegalObjects = illegalObjects + cmds.listRelatives(illegalObjects, p = True)
        
        for i in illegalObjects:
            if i in res:
                res.remove(i)
        
        illegalObjects = cmds.ls(res, s = True)
        
        for x in illegalObjects:
            if x in res:
                res.remove(x)

        return res


    #-----------------------------------Update Input Queries-----------------------------------#
    def updateSourceList(self, list=[]):
        oldList = cmds.textScrollList(self.sourceList, query = True, ai = True)
        cmds.textScrollList(self.sourceList, edit = True, ra = True)
        if list == []:
            resList = oldList
        else:
            resList = list
        rowNum = len(resList)
        cmds.textScrollList(self.sourceList, edit = True, numberOfRows=rowNum, a = resList)
    def updateCtrlNameInput(self, *args):
        res = cmds.textField(self.ctrlNameInput, query = True, text = True)
        return res
    def updateOffsetNameInput(self, *args):
        res = cmds.textField(self.offsetNameInput, query = True, text = True)
        return res
    def updateRadiusFloat(self, *args):
        res = cmds.floatField(self.radiusFloat, query = True, v = True)
        return res
    def runTest(self, *args):
        usedList = cmds.ls(sl = True)
        self.updateSourceList(usedList)

    #-----------------------------------Radio Collections-----------------------------------#
    def selectionMethod(self, *args):
        selectSlIQ = cmds.radioButton(self.selectMethod1, query = True, sl = True)
        selectHiIQ = cmds.radioButton(self.selectMethod2, query = True, sl = True)
        selectAllIQ = cmds.radioButton(self.selectMethod3, query = True, sl = True)

        if selectSlIQ == True:
            selectType = 'selectSl'
            res = self.listSl()
    
            return [selectType, res]
    
        elif selectHiIQ == True:
            selectType = 'selectHi'
            res = self.listHi()
    
            return [selectType, res]
    
        elif selectAllIQ == True:
            selectType = 'selectAll'
            res = self.listAll()
    
            return [selectType, res]
    
    def selectionStatus(self, *args):
        method = self.funcSort(self.selectionMethod, 0)

        if method == 'selectSl':
            res = self.listSl()
            print('Current object list: ' + str(res))
    
        elif method == 'selectHi':
            res = self.listHi()
            print('Current object list: ' + str(res))
    
        elif method == 'selectAll':
            res = self.listAll()
            print('Current object list: ' + str(res))
    
    def ctrlOrient(self, *args):
        orientX = cmds.radioButton(self.orientX, query = True, sl = True)
        orientY = cmds.radioButton(self.orientY, query = True, sl = True)
        orientZ = cmds.radioButton(self.orientZ, query = True, sl = True)

        if orientX == True:
            res = 'x'
    
            return res
    
        elif orientY == True:
            res = 'y'
    
            return res
    
        elif orientZ == True:
            res = 'z'
    
            return res
    
    #-----------------------------------CheckBoxes-----------------------------------#
    def updateConstraintCheck(self, *args):
        res = cmds.checkBox(self.constraintCheck, query = True, v = True)
        return res
    def updateRadiusCheck(self, *args):
        res = cmds.checkBox(self.radiusCheck, query = True, v = True)
        return res
    #----------------------------------------------Functionality----------------------------------------------#
    def addCtrl(self, *args):
        selectionList = self.funcSort(self.selectionMethod, 1)
        trueNameList = []
        
        for i in selectionList:
            if cmds.listRelatives(i, f = True) == None:
                try:
                    parent = cmds.listRelatives(i, p = True, f = True)
                    fullPath = cmds.listRelatives(parent, f = True)
                    fullPath = fullPath[0].split('|')
                except TypeError:
                    fullPath = i
            else:
                fullPath = cmds.listRelatives(i, f = True)
                fullPath = fullPath[0].split('|')[:-1]
            
            hiParent = cmds.listRelatives(i, p = True)
            if cmds.listRelatives(i, p = True) == None:
                hiParent = '0'
            else:
                hiParent = hiParent[0]
            depth = len(fullPath)
            trueNameList = trueNameList + [(i, depth, hiParent)]
        
        # Sorting list by path depth: We don't want our renaming reference to be changed mid-operation,
        # as it would cause problems down the hierarchy when renaming other objects
        depthNameList = sorted(trueNameList, key=lambda tup: tup[1], reverse = 1)
        controlList = []
        for i in depthNameList:
            _obj, _depth, _parent = i
            
            useCustomRadius = self.updateRadiusCheck()
            ctrlName = self.updateCtrlNameInput()
            offsetName = self.updateOffsetNameInput()
            orient = self.ctrlOrient()

            bone = str(_obj)
            ctrl = ctrlName + bone
            offset = offsetName + ctrl
            
            #Custom radius for certain bones
            boneDict = {
                        'head':2,
                        'neck':2,
                        'shoulder':2,
                        'clavicle':2,
                        'wrist':1.35,
                        'hand':1.5,
                        'finger':0.35,
                        'fing':0.35,
                        'thumb':0.35,
                        'index':0.35,
                        'middle':0.35,
                        'ring':0.35,
                        'pinky':0.35,
                        'chest':3.5,
                        'spine':3,
                        'pelvis':4.2,
                        'hip':3,
                        'root':5,
                        'thigh':1.5,
                        'thig':1.5,
                        'foot':1.35,
                        'toes':0.7
                        }
            
            rMultiplier = self.updateRadiusFloat()
            ctrlRadius = 1 * rMultiplier
            for target,r in boneDict.items():
                if useCustomRadius == True:
                    oldName = _obj.upper().split('|')[-1]

                    n = oldName.find(target.upper())

                    if n >= 0:
                        print('Found name in bone')
                        print(str(r))
                        ctrlRadius = r * rMultiplier
                        break
                    else:
                        continue

            print(ctrlRadius)
            #Make Control
            cmds.circle(n=ctrl, r=ctrlRadius)
            cmds.select(ctrl + '.cv[0:7]', r=True)
            if orient == 'x':
                cmds.rotate(90, 0, 0, a=True, os=True, fo=True, ocp=True)
            elif orient == 'y':
                cmds.rotate(0, 90, 0, a=True, os=True, fo=True, ocp=True)
            elif orient == 'z':
                cmds.rotate(0, 0, 90, a=True, os=True, fo=True, ocp=True)
            cmds.delete(ctrl, constructionHistory=True)
            cmds.select(cl=True)

            #Match bone's transforms and set offset groups
            cmds.group(em=True, n=offset, w=True)
            cmds.parent(ctrl, offset)
            cmds.matchTransform(offset, _obj, scl=False)

            #Set aside for reparenting
            controlList = controlList + [(offset, _depth, _parent)]
            
        for i in controlList:
            _offset, _depth, _parent = i
            
            #Parent Controllers together
            if _parent != '0':
                cmds.parent(_offset, ctrlName + _parent)

    #-----------------------------------Selection-----------------------------------#
    def selectByType(self, t):
        try:
            selectionList = cmds.ls(sl=True)
            if t != 'joint':
                selectionList = cmds.listRelatives(selectionList, c = False, s = True, pa = True)

            cmds.select(selectionList, r = True)

            typeList = cmds.ls(sl = True, typ = t)
            cmds.undo()
            parentList = cmds.listRelatives(typeList, c = False, p = True, pa = True)

            resList = typeList + parentList

            cmds.select(resList, r = True)

            print("Selected \"" + t + "\" type objects from previous selection.")
        except TypeError:
            print("Error: No \"" + t + "\" type object selected.")

    def selectHi(self, *args):
        cmds.select(add=True, hi=True)
        print("Selected hierarchy from previous selection.")
    
    def selectCrv(self, *args):
        self.selectByType('nurbsCurve')
    
    def selectJnt(self, *args):
        self.selectByType('joint')
    
    def selectGeo(self, *args):
        self.selectByType('mesh')
    
def UI():
    buddyRigg_Window()
UI()