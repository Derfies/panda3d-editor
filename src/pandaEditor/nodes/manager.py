from game.nodes.manager import Manager as NodeManager


EDITOR_NODE_MODULES = [
    'pandaEditor.nodes.actor',
    'pandaEditor.nodes.base',
    'pandaEditor.nodes.bulletCharacterControllerNode',
    'pandaEditor.nodes.bulletRigidBodyNode',
    'pandaEditor.nodes.bulletWorld',
    'pandaEditor.nodes.lensNode',
    'pandaEditor.nodes.modelRoot',
    'pandaEditor.nodes.nodePath',
    'pandaEditor.nodes.sceneRoot',
    'pandaEditor.nodes.showbaseDefault',
]


class Manager(NodeManager):

    def __init__(self):
        super().__init__()

        self.create_node_wrappers(EDITOR_NODE_MODULES)
