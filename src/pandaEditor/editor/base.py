from editor.nodes.manager import Manager as NodeManager
from editor.plugins.base import Base as EditorPluginBase
from game.plugins.base import Base as GamePluginBase
from editor.plugins.manager import Manager as PluginManager
from editor.sceneParser import SceneParser
from game.base import Base as GameBase


class Base(GameBase):

    node_manager_cls = NodeManager
    plug_manager_cls = PluginManager
    scene_parser_cls = SceneParser

    def load_plugins(self):
        self.plugin_manager.setCategoriesFilter({
            'editor': EditorPluginBase,
            'game': GamePluginBase,
        })
        super().load_plugins()
