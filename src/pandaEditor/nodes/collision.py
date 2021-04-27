import panda3d.core as pc

from game.nodes.attributes import Attribute


class CollisionNode:

    num_solids = Attribute(
        int,
        pc.CollisionNode.get_num_solids,
        serialise=False,
        node_data=True,
    )
