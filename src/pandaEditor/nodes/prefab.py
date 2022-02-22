from game.nodes.attributes import ProjectAssetTagAttribute
from game.nodes.constants import TAG_NODE_TYPE


class Prefab:

    serialise_descendants = False
    fullpath = ProjectAssetTagAttribute(
        required=True,
        read_only=True,
    )
