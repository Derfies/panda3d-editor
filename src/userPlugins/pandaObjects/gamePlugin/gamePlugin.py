import p3d
from game.plugins.base import Base


class GamePlugin( Base ):
        
    def OnInit( self ):
        from script import Script
        from pandaObject import PandaObject

        self.RegisterPyTagWrapper( p3d.TAG_PANDA_OBJECT, PandaObject )
        self.RegisterPyTagWrapper( 'Script', Script )
        
        # DEBUG
        base.pandaMgr = p3d.PandaManager()