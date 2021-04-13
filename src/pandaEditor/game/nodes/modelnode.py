import panda3d.core as pm

from game.nodes.nodepath import NodePath
from game.nodes.wrappermeta import WrapperMeta


class ModelNode(NodePath, metaclass=WrapperMeta):
    
    type_ = pm.ModelNode
