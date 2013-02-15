import pandac.PandaModules as pm
from panda3d.bullet import BulletBoxShape as BBS

from base import Base
from attributes import Attribute as Attr


class BulletBoxShape( Base ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', BBS )
        Base.__init__( self, *args, **kwargs )
        
        self.initArgs = [pm.Vec3( 0.5, 0.5, 0.5 )]
        
        pAttr = Attr( 'BulletBoxShape' )
        pAttr.children.extend( 
            [
                Attr( 'Half Extents Without Margin', pm.Vec3, BBS.getHalfExtentsWithMargin )
            ]
        )
        self.attributes.append( pAttr )