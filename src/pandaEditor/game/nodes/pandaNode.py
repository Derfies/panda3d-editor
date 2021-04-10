import panda3d.core as pm

try:
    from pandaEditor.editor.nodes.nodePath import NodePath
except ImportError:
    from pandaEditor.game.nodes.nodePath import NodePath


class PandaNode(NodePath):
    
    type_ = pm.PandaNode
