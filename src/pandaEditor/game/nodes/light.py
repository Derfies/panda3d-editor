import panda3d.core as pm
from panda3d.core import Light as PandaLight

from game.nodes.attributes import NodeAttribute
from game.nodes.nodepath import NodePath


class Light(NodePath):

    type_ = PandaLight

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            NodeAttribute(
                'Color',
                pm.Vec4,
                PandaLight.getColor,
                PandaLight.setColor
            ),
            parent='Light'
        )
