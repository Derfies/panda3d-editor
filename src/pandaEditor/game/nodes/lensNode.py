import panda3d.core as pm
from panda3d.core import Lens

from .nodePath import NodePath
from .attributes import Attribute as Attr


class LensNode(NodePath):
    
    type_ = pm.LensNode
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            Attr('Fov', pm.Vec2, Lens.getFov, Lens.setFov, self.GetLens),
            Attr('Near', float, Lens.getNear, Lens.setNear, self.GetLens),
            Attr('Far', float, Lens.getFar, Lens.setFar, self.GetLens),
            parent='LensNode'
        )

    def GetLens(self, np):
        return np.node().getLens()