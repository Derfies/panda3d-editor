import panda3d.core as pm
from panda3d.bullet import BulletCapsuleShape as BCS, ZUp

from .base import Base
from .attributes import Attribute as Attr


class BulletCapsuleShape( Base ):
    
    type_ = BCS
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Radius', float, BCS.getRadius, initDefault=0.5 ),
            Attr( 'Height', float, BCS.getHalfHeight, initDefault=1 ),
            Attr( 'Up', int, initDefault=ZUp ),
            parent='BulletCapsuleShape'
        )