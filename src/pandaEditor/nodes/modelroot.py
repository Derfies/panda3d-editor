import panda3d.core as pc

from game.nodes.attributes import ReadOnlyNodeProjectAssetAttribute


class ModelRoot:

    serialise_descendants = False
    model_path = ReadOnlyNodeProjectAssetAttribute(
        pc.Filename,
        pc.ModelRoot.get_fullpath,
        init_arg=''
    )
