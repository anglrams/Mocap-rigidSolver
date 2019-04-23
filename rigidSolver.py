import maya.cmds as cmd
import maya.mel as mel
import maya.OpenMayaAnim as animat

#Get Selection and duplicate names 
sel= cmd.ls( sl=True)
dsel= [x+"1" for x in sel]
mint= int(animat.MAnimControl.minTime().value())
maxt= int(animat.MAnimControl.maxTime().value())

#RigidBody Name Correction
rigidO= 'rigidBodyLocator'
exst= 0
while cmd.objExists(rigidO):
    exst += 1
    rigidL = [rigidO,exst]
    rigidC = rigidL[0]+str(rigidL[1])
    if not cmd.objExists(rigidC):
        break
        
if cmd.objExists(rigidO):
    rigid = rigidL[0]+str(rigidL[1])
else:
    rigid = rigidO


#Delete Existing window
if cmd.window("acro", exists =True):
        cmd.deleteUI("acro")

#Create Window
mWindow = cmd.window("acro",t='SolidSolver v.01', w=200, h=200)
cmd.columnLayout(adj = True)
cmd.text("RigidSolver v1.0")
cmd.separator(h=50)
cmd.text("Accuracy")

#RigidBody Weights
weights = {}
for marker in sel:
    weights["{0}".format(marker)] = cmd.floatFieldGrp(numberOfFields=1, label=marker, value1=1.0,)

cmd.separator(h=10)
##enter TimeRange
cmd.text("Time Range")
cmd.rowColumnLayout( numberOfColumns=2 )
userMintW = cmd.intFieldGrp(l="startFrame",value1=mint)
userMaxtW = cmd.intFieldGrp(l="endFrame",value1=maxt)
cmd.columnLayout(adj = True)
cmd.separator(h=10)
#Automatic Checkbox
checkie = cmd.checkBox(l="Auto", v=True)

#Run
cmd.button( l= "Run" , c= "runG()")

#Show
cmd.showWindow(mWindow)


#General
def runG():
    automa = cmd.checkBox(checkie, q=True, v=True)
    if automa == True:
        create()
        clean()
    else:
        create()
        delet()

#First Run : Rigid Body, Duplicate, Bake animation        
def create():
    mel.eval('peelSolve2RigidBody()')
    cmd.duplicate(sel)
    fW={}
    userMint = cmd.intFieldGrp(userMintW,q=True ,v=True)[0]
    userMaxt = cmd.intFieldGrp(userMaxtW,q=True ,v=True)[0]
    
    print userMint, userMaxt
    for marker in sel:
        fW["{0}".format(marker)]= cmd.floatFieldGrp(weights[marker], q= True, v=True)
        rB= "RB_"+marker+"_Marker"
        cmd.setAttr( rB+'.weight' , fW[marker][0])
        cmd.pointConstraint( rB , marker+"1" , mo=False )
    
    cmd.bakeResults( dsel , t = (userMint,userMaxt))
    cmd.delete(rigid)
    
def delet():    
    for marker in sel:
        fW={}
        fW["{0}".format(marker)]= cmd.floatFieldGrp(weights[marker], q= True, v=True)
        if fW[marker][0] > 0.5:
            cmd.delete(marker+"1")

#Automatic cleaning
def clean():
        
    userMint = cmd.intFieldGrp(userMintW,q=True ,v=True)[0]
    userMaxt = cmd.intFieldGrp(userMaxtW,q=True ,v=True)[0] 
    fW={}
    for marker in sel:
        fW["{0}".format(marker)]= cmd.floatFieldGrp(weights[marker], q= True, v=True)
        if fW[marker][0] < 0.5:
            cmd.select( marker )
            import mocapCleanup.keyTools as kt;kt.setCurrent('1')
            cmd.select( marker+"1"  )
            cmd.selectKey( marker+"1", t = (userMint,userMaxt), attribute='translate' )
            import mocapCleanup.keyTools as kt;kt.moveToCurrent('1')
    
    cmd.delete(dsel)
        
