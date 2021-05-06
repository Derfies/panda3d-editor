import panda3d.core as pc
from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.attributes import ProjectAssetAttribute
from game.nodes.nongraphobject import NonGraphObject


class Texture(NonGraphObject):

    type_ = pc.Texture
    filename = ProjectAssetAttribute(
        pc.Filename,
        pc.Texture.get_filename,
        pc.Texture.set_filename,
        required=True,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        filename = kwargs.pop('filename', None)
        panda_filename = pc.Filename.from_os_specific(filename)
        texture = get_base().loader.load_texture(panda_filename)
        return super().create(data=texture)
