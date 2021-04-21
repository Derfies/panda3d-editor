import panda3d.core as pc

from game.nodes.attributes import ReadOnlyNodeAttribute


class CollisionNode:

    num_solids = ReadOnlyNodeAttribute( # TODO: Move to editior wrapper.
        int,
        pc.CollisionNode.get_num_solids,
        serialise=False
    )
