import pandac.PandaModules as pm
from panda3d.bullet import BulletBoxShape as BBS

from base import Base
from attributes import Attribute as Attr


class BulletBoxShape( Base ):
    
    type_ = BBS
    initArgs = [pm.Vec3( 0.5, 0.5, 0.5 )]
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Half Extents Without Margin', pm.Vec3, BBS.getHalfExtentsWithMargin ),
            parent='BulletBoxShape'
        )