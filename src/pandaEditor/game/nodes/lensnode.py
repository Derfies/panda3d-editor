import panda3d.core as pm
from panda3d.core import Lens

from game.nodes.attributes import NodeAttribute
from game.nodes.nodepath import NodePath
from game.nodes.wrappermeta import WrapperMeta


class LensNode(NodePath, metaclass=WrapperMeta):
    
    type_ = pm.LensNode
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            NodeAttribute('Fov', pm.Vec2, Lens.getFov, Lens.setFov, self.GetLens),
            NodeAttribute('Near', float, Lens.getNear, Lens.setNear, self.GetLens),
            NodeAttribute('Far', float, Lens.getFar, Lens.setFar, self.GetLens),
            parent='LensNode'
        )

    def GetLens(self, np):
        return np.node().getLens()
