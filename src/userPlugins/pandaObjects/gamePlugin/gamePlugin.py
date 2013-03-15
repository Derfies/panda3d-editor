import p3d
from game.plugins.base import Base


class GamePlugin( Base ):
        
    def OnInit( self ):
        from script import Script
        from pandaObject import PandaObject

        self.RegisterNodeWrapper( 'Script', Script )
        self.RegisterNodeWrapper( p3d.TAG_PANDA_OBJECT, PandaObject )
        
        # Add a PandaManager to the game object.
        base.pandaMgr = p3d.PandaManager()