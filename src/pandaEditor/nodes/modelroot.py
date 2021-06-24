import panda3d.core as pc

from game.nodes.attributes import ProjectAssetAttribute


class ModelRoot:

    serialise_descendants = False
    fullpath = ProjectAssetAttribute(
        pc.Filename,
        pc.ModelRoot.get_fullpath,
        required=True,
        node_data=True,
    )
