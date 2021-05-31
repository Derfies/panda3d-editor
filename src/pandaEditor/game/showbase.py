from direct.showbase.ShowBase import ShowBase as DirectShowBase

from game.nodes.manager import Manager as NodeManager
from game.plugins.manager import Manager as PluginManager
from game.sceneparser import SceneParser
from game.scene import Scene


class ShowBase(DirectShowBase):

    node_manager_cls = NodeManager
    plug_manager_cls = PluginManager
    scene_parser_cls = SceneParser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.node_manager = self.node_manager_cls()
        self.plugin_manager = self.plug_manager_cls()
        self.scene_parser = self.scene_parser_cls()

    def load_plugins(self):
        self.plugin_manager.setPluginPlaces([
            r'C:\Users\Jamie Davies\Documents\git\panda3d-editor\src\plugins',
            r'C:\Users\Jamie Davies\Documents\git\reactor\plugins',
        ])
        self.plugin_manager.collectPlugins()
        self.plugin_manager.on_init()

    def load_scene(self, file_path):
        self.scene = Scene(self, camera=None)
        self.scene.load(file_path)
