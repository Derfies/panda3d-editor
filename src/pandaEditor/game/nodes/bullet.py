import panda3d.core as pc
import panda3d.bullet as pb
from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.attributes import (
    Attribute,
    Connection,
    Connections,
    TagAttribute
)
from game.nodes.nodepath import NodePath
from game.nodes.nongraphobject import NonGraphObject


class BulletBoxShape(NonGraphObject):

    type_ = pb.BulletBoxShape
    halfExtents = Attribute(
        pc.Vec3,
        pb.BulletBoxShape.get_half_extents_with_margin,
        required=True,
    )


class BulletCapsuleShape(NonGraphObject):

    type_ = pb.BulletCapsuleShape
    radius = Attribute(float, pb.BulletCapsuleShape.get_radius, required=True)
    height = Attribute(float, pb.BulletCapsuleShape.get_half_height, required=True)
    up = TagAttribute(int, read_only=True, required=True)


class BulletDebugNode(NodePath):

    type_ = pb.BulletDebugNode


class BulletPlaneShape(NonGraphObject):

    type_ = pb.BulletPlaneShape
    normal = TagAttribute(pc.Vec3, read_only=True, required=True)
    point = TagAttribute(pc.Vec3, read_only=True, required=True)

    @classmethod
    def create(cls, *args, **kwargs):
        plane = pc.Plane(kwargs['normal'], kwargs['point'])
        return super().create(plane=plane)


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
        pc.Vec3,
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


class BulletSphereShape(NonGraphObject):

    type_ = pb.BulletSphereShape
    radius = Attribute(
        float,
        pb.BulletSphereShape.get_radius,
        required=True,
    )


def clear_rigid_bodies(obj):
    for i in range(obj.get_num_rigid_bodies()):
        obj.remove(obj.get_rigid_body(0))


class BulletWorld(NonGraphObject):

    type_ = pb.BulletWorld
    gravity = Attribute(
        pc.Vec3,
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

    def destroy(self):
        if (
            get_base().scene.physics_world is self.data and
            get_base().scene.physics_task in get_base().task_mgr.getAllTasks()
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
