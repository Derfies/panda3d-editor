import game
import plugins
from sceneParser import SceneParser


class Base( game.Base ):
    
    def __init__( self, *args, **kwargs ):
        game.Base.__init__( self, *args, **kwargs )
        
        # Use editor versions for some systems.
        self.pluginMgr = plugins.Manager( self )
        self.scnParser = SceneParser()