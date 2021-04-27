import panda3d.core as pm
import panda3d.bullet as pb
from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.attributes import Attribute, Connection, Connections
from game.nodes.base import Base
from game.nodes.nodepath import NodePath


class BulletSphereShape(Base):

    type_ = pb.BulletSphereShape
    radius = Attribute(
        float,
        pb.BulletSphereShape.get_radius,
        init_arg=0.5,
    )


class BulletBoxShape(Base):

    type_ = pb.BulletBoxShape
    half_extents = Attribute(
        pm.Vec3,
        pb.BulletBoxShape.get_half_extents_with_margin,
        init_arg=pm.Vec3(0.5, 0.5, 0.5),
        init_arg_name='halfExtents',
    )


class BulletCapsuleShape(Base):

    type_ = pb.BulletCapsuleShape
    radius = Attribute(float, pb.BulletCapsuleShape.get_radius, init_arg=0.5)
    height = Attribute(float, pb.BulletCapsuleShape.get_half_height, init_arg=1)
    up = Attribute(int, init_arg=pb.ZUp)


class BulletCharacterControllerNode(NodePath):

    type_ = pb.BulletCharacterControllerNode
    shape = Attribute(
        pb.BulletCapsuleShape,
        init_arg=pb.BulletCapsuleShape(0.4, 1.75 - 2 * 0.4, pb.ZUp)
    )
    step_height = Attribute(float, init_arg=0.4)


class BulletDebugNode(NodePath):

    type_ = pb.BulletDebugNode

    @classmethod
    def create(cls, *args, **kwargs):
        comp = super().create(*args, **kwargs)
        comp.show_wireframe = True
        comp.data.show()
        return comp


class BulletPlaneShape(Base):

    type_ = pb.BulletPlaneShape
    normal = Attribute(pm.Vec3, init_arg=pm.Vec3(0, 0, 1))
    constant = Attribute(int, init_arg=0)


def clear_shapes(obj):
    num_shapes = obj.get_num_shapes()
    for i in range(num_shapes):
        obj.remove_shape(obj.get_shape(0))


class BulletRigidBodyNode(NodePath):

    type_ = pb.BulletRigidBodyNode
    angular_dampening = Attribute(
        float,
        pb.BulletRigidBodyNode.getAngularDamping,
        pb.BulletRigidBodyNode.setAngularDamping,
        node_data=True,
    )
    gravity = Attribute(
        pm.Vec3,
        pb.BulletRigidBodyNode.getGravity,
        pb.BulletRigidBodyNode.setGravity,
        node_data=True,
    )
    mass = Attribute(
        float,
        pb.BulletRigidBodyNode.get_mass,
        pb.BulletRigidBodyNode.set_mass,
        node_data=True,
    )
    shapes = Connections(
        pb.BulletShape,
        pb.BulletRigidBodyNode.get_shapes,
        pb.BulletRigidBodyNode.add_shape,
        clear_shapes,
        node_data=True,
    )


def clear_rigid_bodies(obj):
    for i in range(obj.get_num_rigid_bodies()):
        obj.remove(obj.get_rigid_body(0))


def clear_characters(obj):
    for i in range(obj.get_num_characters()):
        obj.remove(obj.get_character(0))


class BulletWorld(Base):

    type_ = pb.BulletWorld
    gravity = Attribute(
        pm.Vec3,
        pb.BulletWorld.get_gravity,
        pb.BulletWorld.set_gravity,
    )
    debug_node = Connection(
        pb.BulletDebugNode,
        pb.BulletWorld.get_debug_node,
        pb.BulletWorld.set_debug_node,
        pb.BulletWorld.clear_debug_node,
        node_target=True,
    )
    rigid_bodies = Connections(
        pb.BulletRigidBodyNode,
        pb.BulletWorld.get_rigid_bodies,
        pb.BulletWorld.attach,
        clear_rigid_bodies,
        node_target=True,
    )
    characters = Connections(
        pb.BulletRigidBodyNode,
        pb.BulletWorld.get_characters,
        pb.BulletWorld.attach,
        clear_characters,
        node_target=True,
    )

    def destroy(self):
        if (
            get_base().scene.physics_world is self.data and
            get_base().scene.physics_task in taskMgr.getAllTasks()
        ):
            self.disable_physics()

    def enable_physics(self):

        def update(task):
            dt = globalClock.getDt()
            self.data.doPhysics(dt)
            return task.cont

        get_base().scene.physics_task = get_base().task_mgr.add(update, 'update')

    def disable_physics(self):
        get_base().task_mgr.remove(get_base().scene.physics_task)
