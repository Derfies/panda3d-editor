from panda3d.bullet import BulletWorld as BW
from panda3d.bullet import BulletRigidBodyNode as BRBN

from game.nodes.attributes import (
    Attribute,
    Connection,
    NodeAttribute,
    NodePathTargetConnectionList,
)


class BulletWorld:
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        i = self.attributes.index(self.FindProperty('rigidBody'))
        self.AddAttributes(Attribute('Num Rigid Bodies', int, BW.getNumRigidBodies, w=False), index=i)
    
    def SetDefaultValues(self):
        super().SetDefaultValues()
        
        # Set this world as the default physics world if one has not already
        # been set.
        if base.scene.physicsWorld is None:
            cnnctn = Connection('PhysicsWorld', None, base.scene.GetPhysicsWorld, base.scene.SetPhysicsWorld, base.scene.ClearPhysicsWorld, srcComp=base.scene)
            cnnctn.Connect(self.data)


class BulletCharacterControllerNode:

    def SetDefaultValues(self):
        super().SetDefaultValues()

        # Attempt to connect this node to the physics world if here is one.
        if base.scene.physicsWorld is not None:
            cnnctn = NodePathTargetConnectionList('Character', None, None, BW.attachCharacter,
                                None, BW.removeCharacter,
                                base.scene.physicsWorld)
            cnnctn.Connect(self.data)


class BulletRigidBodyNode:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        i = self.attributes.index(self.FindProperty('shapes'))
        self.AddAttributes(NodeAttribute ('Num Shapes', int, BRBN.getNumShapes, w=False), index=i)
        self.AddAttributes(NodeAttribute ('Debug Enabled', bool, BRBN.isDebugEnabled, BRBN.setDebugEnabled, w=False))

    def SetDefaultValues(self):
        super().SetDefaultValues()

        # Attempt to connect this node to the physics world if here is one.
        if base.scene.physicsWorld is not None:
            cnnctn = NodePathTargetConnectionList('Rigid Body', None, None, BW.attachRigidBody,
                                None, BW.removeRigidBody,
                                base.scene.physicsWorld)
            cnnctn.Connect(self.data)
