from . import nodes
from . import plugins
from .scene import Scene
from .sceneParser import SceneParser


class Base( object ):
    
    def __init__( self ):
        base.game = self
        self.nodeMgr = nodes.Manager()
        self.pluginMgr = plugins.Manager( self )
        self.scnParser = SceneParser()
        
    def OnInit( self ):
        pass
        #self.pluginMgr.Load()
        
    def Load( self, filePath ):
        self.scene = Scene( self, filePath=filePath, camera=None )
        self.scnParser.Load( self.scene.rootNp, filePath )