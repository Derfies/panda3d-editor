from game.nodes.manager import Manager as NodeManager
from game.plugins.manager import Manager as PluginManager
from game.scene import Scene
from game.sceneParser import SceneParser


class Base:

    node_manager_cls = NodeManager
    plug_manager_cls = PluginManager
    scene_parser_cls = SceneParser
    
    def __init__(self, base):
        self.base = base
        self.node_manager = self.node_manager_cls()
        self.plugin_manager = self.plug_manager_cls(self.base)
        self.scnParser = self.scene_parser_cls()

    def load_plugins(self):
        self.plugin_manager.setPluginPlaces([r"C:\Users\Jamie Davies\Documents\git\panda3d-editor\src\plugins"])
        self.plugin_manager.collectPlugins()
        self.plugin_manager.on_init()

    def Load(self, file_path):
        self.scene = Scene(self, filePath=file_path, camera=None)
        self.scnParser.Load(self.scene.rootNp, file_path)
