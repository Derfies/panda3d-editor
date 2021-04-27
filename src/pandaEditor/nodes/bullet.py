from direct.showbase.PythonUtil import getBase as get_base
from panda3d import bullet

import panda3d.bullet as pb

from game.nodes.attributes import Attribute


TAG_BULLET_DEBUG_WIREFRAME = 'P3D_BulletDebugWireframe'


class BulletWorld:

    num_rigid_bodies = Attribute(
        int,
        bullet.BulletWorld.get_num_rigid_bodies,
        serialise=False,
    )

    def set_default_values(self):
        super().set_default_values()

        # Set this world as the physics world if there isn't already one.
        world = get_base().scene.physics_world
        if world is None:
            scene = get_base().node_manager.wrap(get_base().scene)
            scene.physics_world = self


def get_wireframe(obj):
    return obj.get_python_tag(TAG_BULLET_DEBUG_WIREFRAME)


def set_wireframe(obj, value):
    obj.node().show_wireframe(value)
    obj.set_python_tag(TAG_BULLET_DEBUG_WIREFRAME, value)


class BulletDebugNode:

    show_wireframe = Attribute(bool, get_wireframe, set_wireframe)

    def set_default_values(self):
        super().set_default_values()

        # Connect this node to the physics world if there is one.
        world = get_base().scene.physics_world
        if world is not None:
            world_comp = get_base().node_manager.wrap(world)
            world_comp.debug_node = self


class BulletCharacterControllerNode:

    def set_default_values(self):
        super().set_default_values()

        # Connect this node to the physics world if there is one.
        world = get_base().scene.physics_world
        if world is not None:
            world_comp = get_base().node_manager.wrap(world)
            world_comp.characters.append(self)


class BulletRigidBodyNode:

    debug_enabled = Attribute(
        bool,
        pb.BulletRigidBodyNode.is_debug_enabled,
        pb.BulletRigidBodyNode.set_debug_enabled,
        node_data=True,
        serialise=False,
    )
    num_shapes = Attribute(
        int,
        pb.BulletRigidBodyNode.get_num_shapes,
        serialise=False
    )

    def set_default_values(self):
        super().set_default_values()

        # Connect this node to the physics world if there is one.
        world = get_base().scene.physics_world
        if world is not None:
            world_comp = get_base().node_manager.wrap(world)
            world_comp.rigid_bodies.append(self)
