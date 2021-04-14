import panda3d.core as pm
from panda3d.core import Lens

from game.nodes.attributes import Attribute
from game.nodes.nodepath import NodePath
from game.nodes.othermeta import ComponentMetaClass


class LensNode(NodePath, metaclass=ComponentMetaClass):
    
    type_ = pm.LensNode
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            Attribute('Fov', pm.Vec2, Lens.get_fov, Lens.set_fov, self.get_lens),
            Attribute('Near', float, Lens.get_near, Lens.set_near, self.get_lens),
            Attribute('Far', float, Lens.get_far, Lens.set_far, self.get_lens),
            parent='LensNode'
        )

    def get_lens(self, np):
        return np.node().get_lens()
