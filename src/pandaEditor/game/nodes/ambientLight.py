import panda3d.core as pm

from .light import Light


class AmbientLight( Light ):
    
    type_ = pm.AmbientLight