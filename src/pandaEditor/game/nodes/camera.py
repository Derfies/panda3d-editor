import panda3d.core as pm

from pandaEditor.game.nodes.lensNode import LensNode


class Camera(LensNode):
    
    type_ = pm.Camera
