from direct.showbase.PythonUtil import getBase as get_base
from panda3d import bullet
from panda3d.bullet import BulletWorld as BW
from panda3d.bullet import BulletRigidBodyNode as BRBN

from game.nodes.attributes import (
    Attribute,
    Connection,
    NodeAttribute,
    # NodePathTargetConnectionList,
)


class BulletWorld:

    num_rigid_bodies = Attribute(
        int,
        bullet.BulletWorld.get_num_rigid_bodies,
        serialise=False
    )

    # def set_default_values(self):
    #     super().set_default_values()
    #
    #     # Set this world as the default physics world if one has not already
    #     # been set.
    #     if get_base().scene.physics_world is None:
    #         cnnctn = Connection(
    #             None,
    #             get_base().scene.get_physics_world,
    #             get_base().scene.set_physics_world,
    #             get_base().scene.clear_physics_world
    #         )
    #         cnnctn.connect(self.data)


class BulletCharacterControllerNode:

    def set_default_values(self):
        super().set_default_values()

        # Attempt to connect this node to the physics world if here is one.
        if base.scene.physics_world is not None:
            cnnctn = NodePathTargetConnectionList('Character', None, None, BW.attachCharacter,
                                                  None, BW.removeCharacter,
                                                  base.scene.physics_world)
            cnnctn.connect(self.data)


# class BulletRigidBodyNode:
#
#     pass

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     i = self.attributes.index(self.FindProperty('shapes'))
    #     self.AddAttributes(NodeAttribute ('Num Shapes', int, BRBN.getNumShapes, w=False), index=i)
    #     self.AddAttributes(NodeAttribute ('Debug Enabled', bool, BRBN.isDebugEnabled, BRBN.setDebugEnabled, w=False))

    # def set_default_values(self):
    #     super().set_default_values()
    #
    #     # Attempt to connect this node to the physics world if here is one.
    #     if base.scene.physics_world is not None:
    #         cnnctn = NodePathTargetConnectionList('Rigid Body', None, None, BW.attachRigidBody,
    #                                               None, BW.removeRigidBody,
    #                                               base.scene.physics_world)
    #         cnnctn.Connect(self.data)
