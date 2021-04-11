import panda3d.core as pm

from game.nodes.manager import import_wrapper


LensNode = import_wrapper('nodes.lensNode.LensNode')


class Camera(LensNode):
    
    type_ = pm.Camera
