from panda3d.bullet import BulletWorld as BW

from game.nodes.attributes import Attribute as Attr
from game.nodes.attributes import Connection as Cnnctn
from game.nodes.bulletWorld import BulletWorld as GameBulletWorld


class BulletWorld(GameBulletWorld):
    
    def __init__(self, *args, **kwargs):
        GameBulletWorld.__init__(self, *args, **kwargs)
        
        i = self.attributes.index(self.FindProperty('rigidBody'))
        self.AddAttributes(Attr('Num Rigid Bodies', int, BW.getNumRigidBodies, w=False), index=i)
    
    def SetDefaultValues(self):
        GameBulletWorld.SetDefaultValues(self)
        
        # Set this world as the default physics world if one has not already
        # been set.
        if base.scene.physicsWorld is None:
            cnnctn = Cnnctn('PhysicsWorld', None, base.scene.GetPhysicsWorld, base.scene.SetPhysicsWorld, base.scene.ClearPhysicsWorld, srcComp=base.scene)
            cnnctn.Connect(self.data)


from panda3d.bullet import BulletWorld as BW

from game.nodes.attributes import NodePathTargetConnectionList as CnnctnList
from game.nodes.bulletCharacterControllerNode import BulletCharacterControllerNode as GameBulletCharacterControllerNode


class BulletCharacterControllerNode(GameBulletCharacterControllerNode):

    def SetDefaultValues(self):
        GameBulletCharacterControllerNode.SetDefaultValues(self)

        # Attempt to connect this node to the physics world if here is one.
        if base.scene.physicsWorld is not None:
            cnnctn = CnnctnList('Character', None, None, BW.attachCharacter,
                                None, BW.removeCharacter,
                                base.scene.physicsWorld)
            cnnctn.Connect(self.data)


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
