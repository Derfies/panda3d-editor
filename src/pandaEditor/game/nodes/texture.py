import panda3d.core as pc

from game.nodes.attributes import Attribute
from game.nodes.nongraphobject import NonGraphObject


class Texture(NonGraphObject):

    type_ = pc.Texture
    #name = Attribute(str, read_only=True)
    filename = Attribute(
        pc.Filename,
        pc.Texture.get_filename,
        pc.Texture.set_filename,
    )
