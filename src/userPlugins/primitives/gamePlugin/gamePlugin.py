from box import Box
from cone import Cone
from constants import *
from game.plugins.base import Base


class GamePlugin( Base ):
    
    def __init__( self, *args ):
        Base.__init__( self, *args, sort=-10 )
        
    def OnInit( self ):
        
        # Register primitive types
        self.RegisterNodeWrapper( TAG_BOX, Box )
        self.RegisterNodeWrapper( TAG_CONE, Cone )