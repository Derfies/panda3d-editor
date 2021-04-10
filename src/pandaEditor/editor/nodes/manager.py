from pandaEditor.game.nodes.manager import Manager as NodeManager


EDITOR_NODE_MODULES = [
    'pandaEditor.editor.nodes.modelRoot',
]


class Manager(NodeManager):

    def __init__(self):
        super().__init__()

        self.create_node_wrappers(EDITOR_NODE_MODULES)
