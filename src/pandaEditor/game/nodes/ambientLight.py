import panda3d.core as pm

from game.nodes.light import Light


class AmbientLight(Light):
    
    type_ = pm.AmbientLight
