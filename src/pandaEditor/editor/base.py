from editor.nodes.manager import Manager as NodeManager
from editor.plugins.manager import Manager as PluginManager
from editor.sceneParser import SceneParser
from game.base import Base as GameBase


class Base(GameBase):

    node_manager_cls = NodeManager
    plugin_manager_cls = PluginManager
    scene_parser_cls = SceneParser
