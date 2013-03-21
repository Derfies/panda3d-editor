import p3d
from constants import *
from game.plugins.base import Base


class GamePlugin( Base ):
        
    def OnInit( self ):
        from script import Script
        from pandaObject import PandaObject

        self.RegisterNodeWrapper( TAG_SCRIPT, Script )
        self.RegisterNodeWrapper( TAG_PANDA_OBJECT, PandaObject )
        
        # Add a PandaManager to the game object.
        base.pandaMgr = p3d.PandaManager()