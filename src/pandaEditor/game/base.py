import nodes
import plugins
from sceneParser import SceneParser


class Base( object ):
    
    def __init__( self ):
        base.game = self
        self.nodeMgr = nodes.Manager()
        self.pluginMgr = plugins.Manager( self )
        self.scnParser = SceneParser()
        
    def OnInit( self ):
        self.pluginMgr.Load()