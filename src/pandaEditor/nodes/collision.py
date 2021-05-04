import panda3d.core as pc

from game.nodes.attributes import Attribute


class CollisionBox:

    default_values = {
        'min': pc.Point3(-0.5, -0.5, -0.5),
        'max': pc.Point3(0.5, 0.5, 0.5),
    }


class CollisionCapsule:

    default_values = {
        'a': pc.Point3(0),
        'db': pc.Point3(0, 0, 1),
        'radius': 0.5,
    }


class CollisionNode:

    num_solids = Attribute(
        int,
        pc.CollisionNode.get_num_solids,
        serialise=False,
        node_data=True,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        comp = super().create(*args, **kwargs)
        comp.data.show()  # TODO: Expose as editor property
        return comp


class CollisionRay:

    default_values = {
        'origin': pc.Point3(0),
        'direction': pc.Vec3(0, 0, 1),
    }


class CollisionSphere:

    default_values = {
        'center': pc.Point3(0),
        'radius': 0.5,
    }


class CollisionInvSphere:

    default_values = {
        'center': pc.Point3(0),
        'radius': 0.5,
    }
