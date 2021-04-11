import panda3d.core as pm

from game.nodes.manager import import_wrapper


Light = import_wrapper('nodes.light.Light')


class AmbientLight(Light):
    
    type_ = pm.AmbientLight
