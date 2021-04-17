from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.camera import Camera
from game.nodes.modelnode import ModelNode
from game.nodes.nodepath import NodePath
from game.nodes.othermeta import ComponentMetaClass


class Render(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        comp = cls(get_base().render)
        comp.set_up_node_path()
        return comp

    @property
    def parent(self):
        return get_base().node_manager.wrap(get_base().scene)

    @parent.setter
    def parent(self, value):

        # Render is a default Panda NodePath which shouldn't be parented to
        # anything.
        pass


class BaseCamera(ModelNode, metaclass=ComponentMetaClass):

    @classmethod
    def create(cls, *args, **kwargs):
        comp = cls(get_base().camera)
        comp.set_up_node_path()
        return comp


class BaseCam(Camera, metaclass=ComponentMetaClass):

    @classmethod
    def create(cls, *args, **kwargs):
        comp = cls(get_base().cam)
        comp.set_up_node_path()
        return comp


class Render2d(NodePath, metaclass=ComponentMetaClass):

    @classmethod
    def create(cls, *args, **kwargs):
        comp = cls(get_base().render2d)
        comp.set_up_node_path()
        return comp

    @property
    def parent(self):
        return get_base().node_manager.wrap(get_base().scene)

    @parent.setter
    def parent(self, value):

        # Render2d is a default Panda NodePath which shouldn't be parented to
        # anything.
        pass
    

class Aspect2d(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        comp = cls(get_base().aspect2d)
        comp.set_up_node_path()
        return comp
    

class Pixel2d(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        comp = cls(get_base().pixel2d)
        comp.set_up_node_path()
        return comp
    

class Camera2d(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        comp = cls(get_base().camera2d)
        comp.set_up_node_path()
        return comp
    

class Cam2d(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        comp = cls(get_base().cam2d)
        comp.set_up_node_path()
        return comp
