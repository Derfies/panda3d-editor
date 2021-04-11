import panda3d.core as pm

from game.nodes.manager import import_wrapper


NodePath = import_wrapper('nodes.nodePath.NodePath')


class PandaNode(NodePath):
    
    type_ = pm.PandaNode
