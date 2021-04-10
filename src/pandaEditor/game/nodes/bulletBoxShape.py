import panda3d.core as pm
from panda3d.bullet import BulletBoxShape as BBS

from .base import Base
from .attributes import Attribute as Attr


class BulletBoxShape( Base ):
    
    type_ = BBS
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Half Extents', pm.Vec3, BBS.getHalfExtentsWithMargin, 
                  initDefault=pm.Vec3( 0.5, 0.5, 0.5 ) ),
            parent='BulletBoxShape'
        )