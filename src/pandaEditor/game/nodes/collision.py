import panda3d.core as pc

from game.nodes.attributes import Attribute, Connections
from game.nodes.base import Base
from game.nodes.nodepath import NodePath


class CollisionNode(NodePath):
    
    type_ = pc.CollisionNode
    solids = Connections(
        pc.CollisionSolid,
        pc.CollisionNode.get_solids,
        pc.CollisionNode.add_solid,
        pc.CollisionNode.clear_solids,
        node_data=True,
    )
    
    @classmethod
    def create(cls, *args, **kwargs):
        comp = super().create(*args, **kwargs)
        comp.data.show()    # TODO: Expose as editor property
        return comp


class CollisionBox(Base):
    
    type_ = pc.CollisionBox
    x = Attribute(float, init_arg=0.5)
    y = Attribute(float, init_arg=0.5)
    z = Attribute(float, init_arg=0.5)
    center = Attribute(
        pc.Point3,
        pc.CollisionBox.get_center,
        pc.CollisionBox.set_center,
        init_arg=pc.Point3(0),
    )


class CollisionRay(Base):
    
    type_ = pc.CollisionRay
    origin = Attribute(
        pc.Point3,
        pc.CollisionRay.get_origin,
        pc.CollisionRay.set_origin,
        init_arg=pc.Point3(0),
    )
    direction = Attribute(
        pc.Vec3,
        pc.CollisionRay.get_direction,
        pc.CollisionRay.set_direction,
        init_arg=pc.Vec3(0, 0, 1),
    )


class CollisionSphere(Base):
    
    type_ = pc.CollisionSphere
    center = Attribute(
        pc.Point3,
        pc.CollisionSphere.get_center,
        pc.CollisionSphere.set_center,
        init_arg=pc.Point3(0),
    )
    radius = Attribute(
        float,
        pc.CollisionSphere.get_radius,
        pc.CollisionSphere.set_radius,
        init_arg=0.5,
    )


class CollisionInvSphere(CollisionSphere):
    
    type_ = pc.CollisionInvSphere


class CollisionCapsule(Base):
    
    type_ = pc.CollisionCapsule
    point_a = Attribute(
        pc.Point3,
        pc.CollisionCapsule.get_point_a,
        pc.CollisionCapsule.set_point_a,
        init_arg=pc.Point3(0),
        init_arg_name='a',
    )
    point_b = Attribute(
        pc.Point3,
        pc.CollisionCapsule.get_point_b,
        pc.CollisionCapsule.set_point_b,
        init_arg=pc.Point3(0, 0, 1),
        init_arg_name='db',
    )
    radius = Attribute(
        float,
        pc.CollisionCapsule.get_radius,
        pc.CollisionCapsule.set_radius,
        init_arg=0.5,
    )
