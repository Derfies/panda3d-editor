import panda3d.core as pm

try:
    from pandaEditor.editor.nodes.nodePath import NodePath
except ImportError:
    print('import failed')
    from pandaEditor.game.nodes.nodePath import NodePath


class ModelNode(NodePath):
    
    type_ = pm.ModelNode
