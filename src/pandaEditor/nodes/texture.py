import panda3d.core as pc

from game.nodes.attributes import ProjectAssetAttribute


class Texture:

    type_ = pc.Texture
    filename = ProjectAssetAttribute(
        pc.Filename,
        pc.Texture.get_filename,
        required=True,
    )
