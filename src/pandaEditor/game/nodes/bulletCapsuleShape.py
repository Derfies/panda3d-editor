import pandac.PandaModules as pm
from panda3d.bullet import BulletCapsuleShape as BCS

from base import Base
from attributes import Attribute as Attr


class BulletCapsuleShape( Base ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', BCS )
        Base.__init__( self, *args, **kwargs )
        
        self.initArgs = [pm.Vec3( 0.5, 0.5, 0.5 )]
        
        pAttr = Attr( 'BulletCapsuleShape' )
        pAttr.children.extend( 
            [
                #Attr( 'Half Extents Without Margin', pm.Vec3, BBS.getHalfExtentsWithMargin )
            ]
        )
        self.attributes.append( pAttr )