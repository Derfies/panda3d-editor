import panda3d.core as pm

from game.nodes.nodepath import NodePath
from game.nodes.componentmetaclass import ComponentMetaClass


class ModelNode(NodePath, metaclass=ComponentMetaClass):
    
    type_ = pm.ModelNode
