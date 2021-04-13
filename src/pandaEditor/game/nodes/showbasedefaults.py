from game.nodes.camera import Camera
from game.nodes.modelnode import ModelNode
from game.nodes.nodepath import NodePath
from game.nodes.wrappermeta import WrapperMeta


class Render(NodePath, metaclass=WrapperMeta):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.render)
        wrpr.SetupNodePath()
        return wrpr
    
    def SetParent(self, pComp):
        
        # Render is a default Panda NodePath which shouldn't be parented to
        # anything.
        pass


class BaseCamera(ModelNode, metaclass=WrapperMeta):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.camera)
        wrpr.SetupNodePath()
        return wrpr


class BaseCam(Camera, metaclass=WrapperMeta):

    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.cam)
        wrpr.SetupNodePath()
        return wrpr


class Render2d(NodePath, metaclass=WrapperMeta):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.render2d)
        wrpr.SetupNodePath()
        return wrpr
    
    def SetParent(self, pComp):
        
        # Render2d is a default Panda NodePath which shouldn't be parented to
        # anything.
        pass
    

class Aspect2d(NodePath, metaclass=WrapperMeta):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.aspect2d)
        wrpr.SetupNodePath()
        return wrpr
    

class Pixel2d(NodePath, metaclass=WrapperMeta):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.pixel2d)
        wrpr.SetupNodePath()
        return wrpr
    

class Camera2d(NodePath, metaclass=WrapperMeta):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.camera2d)
        wrpr.SetupNodePath()
        return wrpr
    

class Cam2d(NodePath, metaclass=WrapperMeta):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.cam2d)
        wrpr.SetupNodePath()
        return wrpr
