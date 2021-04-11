from game.nodes.manager import Manager as NodeManager
from game.plugins.manager import Manager as PluginManager
from game.scene import Scene
from game.sceneParser import SceneParser


class Base:

    node_manager_cls = NodeManager
    plugin_manager_cls = PluginManager
    scene_parser_cls = SceneParser
    
    def __init__(self):
        base.game = self
        self.nodeMgr = self.node_manager_cls()
        self.pluginMgr = self.plugin_manager_cls(self)
        self.scnParser = self.scene_parser_cls()
        
    def OnInit(self):
        pass
        #self.pluginMgr.Load()
        
    def Load(self, file_path):
        self.scene = Scene(self, filePath=file_path, camera=None)
        self.scnParser.Load(self.scene.rootNp, file_path)