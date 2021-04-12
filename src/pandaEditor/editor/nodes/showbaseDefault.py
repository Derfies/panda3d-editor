from editor.nodes.constants import TAG_IGNORE
from game.nodes.pandaNode import PandaNode
from game.nodes.modelNode import ModelNode
from game.nodes.camera import Camera
from game.nodes.showbaseDefault import (
    Aspect2d as GameAspect2d,
    BaseCam as GameBaseCam,
    BaseCamera as GameBaseCamera,
    Cam2d as GameCam2d,
    Camera2d as GameCamera2d,
    Pixel2d as GamePixel2d,
    Render as GameRender,
    Render2d as GameRender2d,
)


class Render(GameRender):
    
    def GetParent(self):
        return base.node_manager.Wrap(base.scene)
    
    @classmethod
    def GetDefaultPropertyData(cls):
        return PandaNode.Create(name='render').GetPropertyData()
    

class BaseCamera(GameBaseCamera):
    
    @classmethod
    def GetDefaultPropertyData(cls):
        return ModelNode.Create(name='camera').GetPropertyData()
    

class BaseCam(GameBaseCam):
    
    @classmethod
    def GetDefaultPropertyData(cls):
        return Camera.Create(name='cam').GetPropertyData()
    

class Render2d(GameRender2d):
    
    def GetParent(self):
        return base.node_manager.Wrap(base.scene)
    
    @classmethod
    def GetDefaultPropertyData(cls):
        return PandaNode.Create(name='render2d').GetPropertyData()
    

class Aspect2d(GameAspect2d):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = super(Aspect2d, cls).Create(*args, **kwargs)
        
        # Tag all NodePaths under this node with the ignore tag. They are used
        # to help caculate the aspect ratio and don't need to be saved out or
        # edited. As long as this NodePath wrapper is created before parenting
        # any other NodePaths the user may have created we shouldn't get into
        # much trouble.
        for childNp in wrpr.data.getChildren():
            childNp.setPythonTag(TAG_IGNORE, True)
        return wrpr
    
    @classmethod
    def GetDefaultPropertyData(cls):
        return PandaNode.Create(name='aspect2d').GetPropertyData()
    

class Pixel2d(GamePixel2d):
    
    @classmethod
    def GetDefaultPropertyData(cls):
        return PandaNode.Create(name='pixel2d').GetPropertyData()
    

class Camera2d(GameCamera2d):
    
    @classmethod
    def GetDefaultPropertyData(cls):
        return PandaNode.Create(name='camera2d').GetPropertyData()
    

class Cam2d(GameCam2d):
    
    @classmethod
    def GetDefaultPropertyData(cls):
        return Camera.Create(name='cam2d').GetPropertyData()
