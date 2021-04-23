import panda3d.core as pm
from panda3d.core import Lens

from game.nodes.attributes import Attribute
from game.nodes.nodepath import NodePath
from game.nodes.componentmetaclass import ComponentMetaClass


class LensNodeAttribute(Attribute):

    def _get_data(self, instance):
        return super()._get_data(instance).node().get_lens()


class LensNode(NodePath, metaclass=ComponentMetaClass):
    
    type_ = pm.LensNode
    fov = LensNodeAttribute(pm.Vec2, Lens.get_fov, Lens.set_fov)
    near = LensNodeAttribute(float, Lens.get_near, Lens.set_near)
    far = LensNodeAttribute(float, Lens.get_far, Lens.set_far)
