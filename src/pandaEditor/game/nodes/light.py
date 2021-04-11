import panda3d.core as pm
from panda3d.core import Light as L

from game.nodes.manager import import_wrapper


Attr = import_wrapper('nodes.attributes.NodeAttribute')
NodePath = import_wrapper('nodes.nodePath.NodePath')


class Light(NodePath):

    type_ = L

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attr('Color', pm.Vec4, L.getColor, L.setColor),
            parent='Light'
        )
