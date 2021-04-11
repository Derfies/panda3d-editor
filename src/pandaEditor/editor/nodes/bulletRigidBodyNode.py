from panda3d.bullet import BulletWorld as BW
from panda3d.bullet import BulletRigidBodyNode as BRBN

from game.nodes.bulletRigidBodyNode import BulletRigidBodyNode as GameBulletRigidBodyNode
from game.nodes.attributes import (
    NodeAttribute as Attr, 
    NodePathTargetConnectionList as CnnctnList
)


class BulletRigidBodyNode(GameBulletRigidBodyNode):
    
    def __init__(self, *args, **kwargs):
        GameBulletRigidBodyNode.__init__(self, *args, **kwargs)
        
        i = self.attributes.index(self.FindProperty('shapes'))
        self.AddAttributes(Attr('Num Shapes', int, BRBN.getNumShapes, w=False), index=i)
        self.AddAttributes(Attr('Debug Enabled', bool, BRBN.isDebugEnabled, BRBN.setDebugEnabled, w=False))
        
    def SetDefaultValues(self):
        GameBulletRigidBodyNode.SetDefaultValues(self)
        
        # Attempt to connect this node to the physics world if here is one.
        if base.scene.physicsWorld is not None:
            cnnctn = CnnctnList('Rigid Body', None, None, BW.attachRigidBody, 
                                 None, BW.removeRigidBody, 
                                 base.scene.physicsWorld)
            cnnctn.Connect(self.data)
