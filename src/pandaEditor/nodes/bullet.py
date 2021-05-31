from direct.showbase.PythonUtil import getBase as get_base
from panda3d import bullet

import panda3d.bullet as pb
import panda3d.core as pc

from game.nodes.attributes import Attribute


TAG_BULLET_DEBUG_WIREFRAME = 'P3D_BulletDebugWireframe'


class BulletBoxShape:

    default_values = {
        'halfExtents': pc.Vec3(0.5, 0.5, 0.5),
    }


class BulletCapsuleShape:

    default_values = {
        'radius': 0.5,
        'height': 1,
        'up': pb.ZUp,
    }

    @classmethod
    def create(cls, *args, **kwargs):
        comp = super().create(cls, *args, **kwargs)
        comp.up = kwargs['up']
        return comp


def get_wireframe(obj):
    return obj.get_python_tag(TAG_BULLET_DEBUG_WIREFRAME)


def set_wireframe(obj, value):
    obj.node().show_wireframe(value)
    obj.set_python_tag(TAG_BULLET_DEBUG_WIREFRAME, value)


class BulletDebugNode:

    show_wireframe = Attribute(bool, get_wireframe, set_wireframe)

    def set_default_values(self):
        super().set_default_values()

        # Show debug wireframe by default.
        self.show_wireframe = True
        self.data.show()    # This appears to be necessary??

        # Connect this node to the physics world if there is one.
        world = get_base().scene.physics_world
        if world is not None:
            world_comp = get_base().node_manager.wrap(world)
            world_comp.debug_node = self


class BulletPlaneShape:

    default_values = {
        'normal': pc.Vec3(0, 0, 1),
        'point': pc.Vec3(0, 0, 0),
    }

    @classmethod
    def create(cls, *args, **kwargs):
        comp = super().create(cls, *args, **kwargs)
        comp.normal = kwargs['normal']
        comp.point = kwargs['point']
        return comp


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
        node_data=True,
        serialise=False
    )

    def set_default_values(self):
        super().set_default_values()

        # Connect this node to the physics world if there is one.
        world = get_base().scene.physics_world
        if world is not None:
            world_comp = get_base().node_manager.wrap(world)
            world_comp.rigid_bodies.append(self)


class BulletSphereShape:

    default_values = {
        'radius': 0.5,
    }


class BulletWorld:

    num_rigid_bodies = Attribute(
        int,
        bullet.BulletWorld.get_num_rigid_bodies,
        serialise=False,
    )

    def set_default_values(self):
        super().set_default_values()

        # Use realistic gravity value as a default.
        self.gravity = pc.Vec3(0, 0, -9.81)

        # Set this world as the physics world if there isn't already one.
        world = get_base().scene.physics_world
        if world is None:
            scene = get_base().node_manager.wrap(get_base().scene)
            scene.physics_world = self
