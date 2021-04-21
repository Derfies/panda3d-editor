import panda3d.core as pm
import panda3d.bullet as pb
from panda3d.bullet import BulletBoxShape as BBS
from panda3d.bullet import BulletCapsuleShape as BCS
from panda3d.bullet import BulletWorld as BW
from panda3d.bullet import BulletDebugNode as BDN
from panda3d.bullet import BulletCharacterControllerNode as BCCN
from panda3d.bullet import BulletPlaneShape as BPS
from panda3d.bullet import BulletRigidBodyNode as BRBN, BulletShape as BS
from panda3d.bullet import ZUp

from game.nodes.attributes import (
    Base as BaseAttribute,
    Attribute,
    ReadOnlyAttribute,
    Connection,
    Connections,
    NodeAttribute,
    NodeConnection,
    ToNodeConnection,
    ToNodesConnection,
    NodeToNodesConnection,
    NodeConnections,
    # NodePathSourceConnections,
    # NodePathTargetConnection,
    # NodePathTargetConnections,
)
from game.nodes.base import Base
from game.nodes.nodepath import NodePath


TAG_BULLET_DEBUG_WIREFRAME = 'P3D_BulletDebugWireframe'


class BulletSphereShape(Base):

    type_ = pb.BulletSphereShape
    radius = ReadOnlyAttribute(
        float,
        pb.BulletSphereShape.get_radius,
        init_arg=0.5,
    )


class BulletBoxShape(Base):

    type_ = pb.BulletBoxShape
    half_extents = ReadOnlyAttribute(
        pm.Vec3,
        pb.BulletBoxShape.get_half_extents_with_margin,
        init_arg=pm.Vec3(0.5, 0.5, 0.5),
        init_arg_name='halfExtents',
    )


class BulletCapsuleShape(Base):

    type_ = pb.BulletCapsuleShape
    radius = ReadOnlyAttribute(float, pb.BulletCapsuleShape.get_radius, init_arg=0.5)
    height = ReadOnlyAttribute(float, pb.BulletCapsuleShape.get_half_height, init_arg=1)
    up = BaseAttribute(int, init_arg=pb.ZUp)


class BulletCharacterControllerNode(NodePath):

    type_ = pb.BulletCharacterControllerNode
    shape = BaseAttribute(
        pb.BulletCapsuleShape,
        init_arg=pb.BulletCapsuleShape(0.4, 1.75 - 2 * 0.4, pb.ZUp)
    )
    step_height = BaseAttribute(float, init_arg=0.4)
    #name = Attribute(str)


class ShowWireframeAttribute(Attribute):

    def __init__(self):
        super().__init__(bool, self.get_wireframe, self.set_wireframe)

    def get_wireframe(self, np):
        return np.get_python_tag(TAG_BULLET_DEBUG_WIREFRAME)

    def set_wireframe(self, np, value):
        np.node().show_wireframe(value)
        np.set_python_tag(TAG_BULLET_DEBUG_WIREFRAME, value)


class BulletDebugNode(NodePath):

    type_ = pb.BulletDebugNode
    show_wireframe = ShowWireframeAttribute()

    @classmethod
    def create(cls, *args, **kwargs):
        comp = super().create(*args, **kwargs)
        comp.show_wireframe.set(True)
        comp.data.show()
        return comp


class BulletPlaneShape(Base):

    type_ = pb.BulletPlaneShape
    normal = BaseAttribute(pm.Vec3, init_arg=pm.Vec3(0, 0, 1))
    constant = BaseAttribute(int, init_arg=0)


class ShapesConnection(NodeConnections):

    def __init__(self):
        super().__init__(
            pb.BulletShape,
            pb.BulletRigidBodyNode.get_shapes,
            pb.BulletRigidBodyNode.add_shape,
            self.clear_shapes,
            None,
        )

    def clear_shapes(self, value):
        num_shapes = self.data.get_num_shapes()
        for i in range(num_shapes):
            shape = self.data.get_shape(0)
            self.data.remove_shape(shape)


class BulletRigidBodyNode(NodePath):

    type_ = pb.BulletRigidBodyNode
    angular_dampening = NodeAttribute(
        float,
        pb.BulletRigidBodyNode.getAngularDamping,
        pb.BulletRigidBodyNode.setAngularDamping,
    )
    gravity = NodeAttribute(
        pm.Vec3,
        pb.BulletRigidBodyNode.getGravity,
        pb.BulletRigidBodyNode.setGravity,
    )
    mass = NodeAttribute(
        float,
        pb.BulletRigidBodyNode.get_mass,
        pb.BulletRigidBodyNode.set_mass,
    )
    shapes = ShapesConnection()


class BulletWorld(Base):

    def _clear_rigid_bodies(comp):
        for i in range(comp.get_num_rigid_bodies()):
            comp.remove_rigid_body(comp.get_rigid_body(0))

    type_ = pb.BulletWorld
    gravity = Attribute(
        pm.Vec3,
        pb.BulletWorld.get_gravity,
        pb.BulletWorld.set_gravity,
    )
    debug_node = ToNodeConnection(
        pb.BulletDebugNode,
        pb.BulletWorld.get_debug_node,
        pb.BulletWorld.set_debug_node,
        pb.BulletWorld.clear_debug_node,
    )
    rigid_bodies = ToNodesConnection(
        pb.BulletRigidBodyNode,
        pb.BulletWorld.get_rigid_bodies,
        pb.BulletWorld.attach_rigid_body,
        _clear_rigid_bodies,
        None,
    )

    def destroy(self):
        if (
            base.scene.physics_world is self.data and
            base.scene.physics_task in taskMgr.getAllTasks()
        ):
            self.DisablePhysics()

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

        base.scene.physics_task = taskMgr.add(update, 'update')

    def DisablePhysics(self):
        taskMgr.remove(base.scene.physics_task)
