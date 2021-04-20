import panda3d.core as pm

from game.nodes.lensnode import LensNode
from game.nodes.componentmetaclass import ComponentMetaClass


class Camera(LensNode, metaclass=ComponentMetaClass):
    
    type_ = pm.Camera
