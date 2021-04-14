from direct.showbase.PythonUtil import getBase as get_base

from nodes.constants import TAG_IGNORE
from game.nodes.camera import Camera
from game.nodes.modelnode import ModelNode
from game.nodes.pandanode import PandaNode


class Render:

    def GetParent(self):
        return get_base().node_manager.Wrap(get_base().scene)

    @classmethod
    def GetDefaultPropertyData(cls):
        return PandaNode.Create(name='render').GetPropertyData()


class BaseCamera:

    @classmethod
    def GetDefaultPropertyData(cls):
        return ModelNode.Create(name='camera').GetPropertyData()


class BaseCam:

    @classmethod
    def GetDefaultPropertyData(cls):
        return Camera.Create(name='cam').GetPropertyData()


class Render2d:

    def GetParent(self):
        return get_base().node_manager.Wrap(get_base().scene)
    
    @classmethod
    def GetDefaultPropertyData(cls):
        return PandaNode.Create(name='render2d').GetPropertyData()
    

class Aspect2d:
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = super(Aspect2d, cls).Create(*args, **kwargs)
        
        # Tag all NodePaths under this node with the ignore tag. They are used
        # to help calculate the aspect ratio and don't need to be saved out or
        # edited. As long as this NodePath wrapper is created before parenting
        # any other NodePaths the user may have created we shouldn't get into
        # much trouble.
        for childNp in wrpr.data.getChildren():
            childNp.setPythonTag(TAG_IGNORE, True)
        return wrpr
    
    @classmethod
    def GetDefaultPropertyData(cls):
        return PandaNode.Create(name='aspect2d').GetPropertyData()
    

class Pixel2d:
    
    @classmethod
    def GetDefaultPropertyData(cls):
        return PandaNode.Create(name='pixel2d').GetPropertyData()
    

class Camera2d:
    
    @classmethod
    def GetDefaultPropertyData(cls):
        return PandaNode.Create(name='camera2d').GetPropertyData()
    

class Cam2d:
    
    @classmethod
    def GetDefaultPropertyData(cls):
        return Camera.Create(name='cam2d').GetPropertyData()
