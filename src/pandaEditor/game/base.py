from yapsy.PluginManager import PluginManager

from game.nodes.manager import Manager as NodeManager
from game.scene import Scene
from game.sceneParser import SceneParser


class Base:

    node_manager_cls = NodeManager
    scene_parser_cls = SceneParser
    
    def __init__(self, base):
        self.base = base
        self.node_manager = self.node_manager_cls()
        self.scnParser = self.scene_parser_cls()

        self.plugin_manager = PluginManager()
        self.plugin_manager.setPluginPlaces([r"C:\Users\Jamie Davies\Documents\git\panda3d-editor\src\plugins"])
        self.plugin_manager.collectPlugins()

    def load_plugins(self):
        # Loop round the plugins and print their names.
        for plugin in self.plugin_manager.getAllPlugins():
            plugin.plugin_object.on_init(self.base)

    def Load(self, file_path):
        self.scene = Scene(self, filePath=file_path, camera=None)
        self.scnParser.Load(self.scene.rootNp, file_path)
