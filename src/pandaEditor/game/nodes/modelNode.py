import panda3d.core as pm

from game.nodes.manager import import_wrapper


NodePath = import_wrapper('nodes.nodePath.NodePath')


class ModelNode(NodePath):
    
    type_ = pm.ModelNode
