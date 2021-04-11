import panda3d.core as pm
from panda3d.bullet import BulletWorld as BW
from panda3d.bullet import BulletDebugNode as BDN
from panda3d.bullet import BulletRigidBodyNode as BRBN
from panda3d.bullet import BulletCharacterControllerNode as BCCN

from game.nodes.manager import import_wrapper


Base = import_wrapper('nodes.base.Base')
Attr = import_wrapper('nodes.attributes.Attribute')
Cnnctn = import_wrapper('nodes.attributes.Connection')
CnnctnList = import_wrapper('nodes.attributes.ConnectionList')


class BulletWorld(Base):
    
    type_ = BW
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            Attr('Gravity', pm.Vec3, BW.getGravity, BW.setGravity),
            CnnctnList('Rigid Body', BRBN, BW.getRigidBodies, BW.attachRigidBody, self.ClearRigidBodies, BW.removeRigidBody, self.data),
            CnnctnList('Character', BCCN, BW.getCharacters, BW.attachCharacter, self.ClearCharacters, BW.removeCharacter, self.data),
            Cnnctn('Debug Node', BDN, self.GetDebugNode, BW.setDebugNode, BW.clearDebugNode, self.data),
            parent='BulletWorld'
       )
        
    def Destroy(self):
        if (base.scene.physicsWorld is self.data and 
             base.scene.physicsTask in taskMgr.getAllTasks()):
            self.DisablePhysics()
        
    def ClearRigidBodies(self, comp):
        for i in range(comp.getNumRigidBodies()):
            comp.removeRigidBody(comp.getRigidBody(0))
            
    def ClearCharacters(self, comp):
        for i in range(comp.getNumCharacters()):
            comp.removeCharacter(comp.getCharacter(0))
            
    def GetDebugNode(self, args):
        pass
    
    def EnablePhysics(self):
        
        def update(task):
          dt = globalClock.getDt()
          self.data.doPhysics(dt)
          return task.cont
        
        base.scene.physicsTask = taskMgr.add(update, 'update')
        
    def DisablePhysics(self):
        taskMgr.remove(base.scene.physicsTask)