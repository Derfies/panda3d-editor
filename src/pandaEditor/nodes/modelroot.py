import panda3d.core as pc

from game.nodes.attributes import ProjectAssetAttribute


class ModelRoot:

    serialise_descendants = False
    model_path = ProjectAssetAttribute(
        pc.Filename,
        pc.ModelRoot.get_fullpath,
        init_arg='',
        node_data=True,
    )
