import p3d
from game.plugins.base import Base
from pandaObject import PandaObject
from script import Script


class GamePlugin( Base ):
        
    def OnInit( self ):
        self.RegisterPyTagWrapper( p3d.TAG_PANDA_OBJECT, PandaObject )
        self.RegisterPyTagWrapper( 'Script', Script )