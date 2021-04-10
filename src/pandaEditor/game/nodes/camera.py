import panda3d.core as pm

from .lensNode import LensNode


class Camera(LensNode):
    
    type_ = pm.Camera
