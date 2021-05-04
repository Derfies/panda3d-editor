from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.camera import Camera
from game.nodes.modelnode import ModelNode
from game.nodes.nodepath import NodePath
from game.nodes.componentmetaclass import ComponentMetaClass


class Render(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        return cls(get_base().render)

    @property
    def parent(self):
        return get_base().node_manager.wrap(get_base().scene)

    @parent.setter
    def parent(self, value):
        pass


class BaseCamera(ModelNode, metaclass=ComponentMetaClass):

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(get_base().camera)


class BaseCam(Camera, metaclass=ComponentMetaClass):

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(get_base().cam)


class Render2d(NodePath, metaclass=ComponentMetaClass):

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(get_base().render2d)

    @property
    def parent(self):
        return get_base().node_manager.wrap(get_base().scene)

    @parent.setter
    def parent(self, value):
        pass
    

class Aspect2d(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        return cls(get_base().aspect2d)
    

class Pixel2d(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        return cls(get_base().pixel2d)
    

class Camera2d(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        return cls(get_base().camera2d)
    

class Cam2d(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        return cls(get_base().cam2d)
