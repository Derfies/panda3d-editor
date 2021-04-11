from game.nodes.manager import Manager as NodeManager


EDITOR_NODE_MODULES = [
    'pandaEditor.editor.nodes.actor',
    'pandaEditor.editor.nodes.base',
    'pandaEditor.editor.nodes.bulletCharacterControllerNode',
    'pandaEditor.editor.nodes.bulletRigidBodyNode',
    'pandaEditor.editor.nodes.bulletWorld',
    'pandaEditor.editor.nodes.lensNode',
    'pandaEditor.editor.nodes.modelRoot',
    'pandaEditor.editor.nodes.nodePath',
    'pandaEditor.editor.nodes.sceneRoot',
    'pandaEditor.editor.nodes.showbaseDefault',
]


class Manager(NodeManager):

    def __init__(self):
        super().__init__()

        self.create_node_wrappers(EDITOR_NODE_MODULES)
