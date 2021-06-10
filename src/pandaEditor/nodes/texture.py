import panda3d.core as pc

from game.nodes.attributes import ProjectAssetAttribute


class Texture:

    fullpath = ProjectAssetAttribute(
        pc.Filename,
        pc.Texture.get_fullpath,
        required=True,
    )

    @property
    def label(self):
        return self.fullpath
