import pandac.PandaModules as pm
from panda3d.bullet import BulletPlaneShape as BPS

from base import Base
from attributes import Attribute as Attr


class BulletPlaneShape( Base ):
    
    type_ = BPS
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Normal', pm.Vec3, initDefault=pm.Vec3( 0, 0, 1 ) ),
            Attr( 'Constant', int, initDefault=0 ),
            parent='BulletBoxShape'
        )