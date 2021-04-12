import panda3d.core as pm

from game.nodes.lensnode import LensNode
from game.nodes.wrappermeta import WrapperMeta


class Camera(LensNode, metaclass=WrapperMeta):
    
    type_ = pm.Camera
