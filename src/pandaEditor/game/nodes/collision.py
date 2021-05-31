import panda3d.core as pc

from game.nodes.attributes import Attribute, Connections
from game.nodes.nodepath import NodePath
from game.nodes.nongraphobject import NonGraphObject


class CollisionBox(NonGraphObject):

    type_ = pc.CollisionBox
    min = Attribute(
        pc.Point3,
        pc.CollisionBox.get_min,
        required=True,
    )
    max = Attribute(
        pc.Point3,
        pc.CollisionBox.get_max,
        required=True,
    )


class CollisionCapsule(NonGraphObject):

    type_ = pc.CollisionCapsule
    a = Attribute(
        pc.Point3,
        pc.CollisionCapsule.get_point_a,
        pc.CollisionCapsule.set_point_a,
        required=True,
    )
    db = Attribute(
        pc.Point3,
        pc.CollisionCapsule.get_point_b,
        pc.CollisionCapsule.set_point_b,
        required=True,
    )
    radius = Attribute(
        float,
        pc.CollisionCapsule.get_radius,
        pc.CollisionCapsule.set_radius,
        required=True,
    )


class CollisionNode(NodePath):
    
    type_ = pc.CollisionNode
    solids = Connections(
        pc.CollisionSolid,
        pc.CollisionNode.get_solids,
        pc.CollisionNode.add_solid,
        pc.CollisionNode.clear_solids,
        node_data=True,
    )


class CollisionRay(NonGraphObject):
    
    type_ = pc.CollisionRay
    origin = Attribute(
        pc.Point3,
        pc.CollisionRay.get_origin,
        pc.CollisionRay.set_origin,
        required=True,
    )
    direction = Attribute(
        pc.Vec3,
        pc.CollisionRay.get_direction,
        pc.CollisionRay.set_direction,
        required=True,
    )


class CollisionSphere(NonGraphObject):
    
    type_ = pc.CollisionSphere
    center = Attribute(
        pc.Point3,
        pc.CollisionSphere.get_center,
        pc.CollisionSphere.set_center,
        required=True,
    )
    radius = Attribute(
        float,
        pc.CollisionSphere.get_radius,
        pc.CollisionSphere.set_radius,
        required=True,
    )


class CollisionInvSphere(CollisionSphere):
    
    type_ = pc.CollisionInvSphere
