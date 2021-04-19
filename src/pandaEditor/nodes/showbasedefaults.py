from game.nodes.camera import Camera
from game.nodes.modelnode import ModelNode
from game.nodes.pandanode import PandaNode
from pandaEditor.nodes.constants import TAG_IGNORE


class Render:

    @classmethod
    def get_default_property_data(cls):
        return PandaNode.create(name='render').get_property_data()


class BaseCamera:

    @classmethod
    def get_default_property_data(cls):
        return ModelNode.create(name='camera').get_property_data()


class BaseCam:

    @classmethod
    def get_default_property_data(cls):
        return Camera.create(name='cam').get_property_data()


class Render2d:
    
    @classmethod
    def get_default_property_data(cls):
        return PandaNode.create(name='render2d').get_property_data()
    

class Aspect2d:
    
    @classmethod
    def create(cls, *args, **kwargs):
        comp = super().create(*args, **kwargs)
        
        # Tag all NodePaths under this node with the ignore tag. They are used
        # to help calculate the aspect ratio and don't need to be saved out or
        # edited. As long as this NodePath wrapper is created before parenting
        # any other NodePaths the user may have created we shouldn't get into
        # much trouble.
        for np in comp.data.get_children():
            np.set_python_tag(TAG_IGNORE, True)
        return comp
    
    @classmethod
    def get_default_property_data(cls):
        return PandaNode.create(name='aspect2d').get_property_data()
    

class Pixel2d:
    
    @classmethod
    def get_default_property_data(cls):
        return PandaNode.create(name='pixel2d').get_property_data()
    

class Camera2d:
    
    @classmethod
    def get_default_property_data(cls):
        return PandaNode.create(name='camera2d').get_property_data()
    

class Cam2d:
    
    @classmethod
    def get_default_property_data(cls):
        return Camera.create(name='cam2d').get_property_data()
