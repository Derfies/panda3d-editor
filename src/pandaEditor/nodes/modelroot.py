import panda3d.core as pc

from game.nodes.attributes import NodeProjectAssetAttribute


class ModelRoot:

    serialise_descendants = False
    model_path = NodeProjectAssetAttribute(
        pc.Filename,
        pc.ModelRoot.get_fullpath,
        init_arg=''
    )
