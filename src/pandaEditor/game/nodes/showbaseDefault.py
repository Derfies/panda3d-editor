from game.nodes.camera import Camera
from game.nodes.manager import import_wrapper
from game.nodes.modelNode import ModelNode


NodePath = import_wrapper('nodes.nodePath.NodePath')


class Render(NodePath):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.render)
        wrpr.SetupNodePath()
        return wrpr
    
    def SetParent(self, pComp):
        
        # Render is a default Panda NodePath which shouldn't be parented to
        # anything.
        pass
    

class BaseCamera(ModelNode):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.camera)
        wrpr.SetupNodePath()
        return wrpr
    

class BaseCam(Camera):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.cam)
        wrpr.SetupNodePath()
        return wrpr
    

class Render2d(NodePath):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.render2d)
        wrpr.SetupNodePath()
        return wrpr
    
    def SetParent(self, pComp):
        
        # Render2d is a default Panda NodePath which shouldn't be parented to
        # anything.
        pass
    

class Aspect2d(NodePath):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.aspect2d)
        wrpr.SetupNodePath()
        return wrpr
    

class Pixel2d(NodePath):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.pixel2d)
        wrpr.SetupNodePath()
        return wrpr
    

class Camera2d(NodePath):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.camera2d)
        wrpr.SetupNodePath()
        return wrpr
    

class Cam2d(NodePath):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.cam2d)
        wrpr.SetupNodePath()
        return wrpr
