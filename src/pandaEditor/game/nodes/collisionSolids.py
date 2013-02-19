import pandac.PandaModules as pm
from pandac.PandaModules import CollisionBox as CB
from pandac.PandaModules import CollisionRay as CR
from pandac.PandaModules import CollisionSphere as CS
from pandac.PandaModules import CollisionInvSphere  as CIS
from pandac.PandaModules import CollisionTube as CT

from base import Base
from attributes import Attribute as Attr


class CollisionBox( Base ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', CB )
        Base.__init__( self, *args, **kwargs )
        
        self.initArgs = [pm.Point3( 0 ), 0.5]
        
        pAttr = Attr( 'Collision Box' )
        pAttr.children.extend( 
            [
                Attr( 'Center', pm.Point3, CB.getCenter, CB.setCenter )
            ]
        )
        self.attributes.append( pAttr )
    

class CollisionRay( Base ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', CR )
        Base.__init__( self, *args, **kwargs )
        
        self.initArgs = [pm.Point3( 0, 0, 0 ), pm.Vec3( 0, 0, 1 )]
        
        pAttr = Attr( 'Collision Ray' )
        pAttr.children.extend( 
            [
                Attr( 'Origin', pm.Point3, CR.getOrigin, CR.setOrigin ),
                Attr( 'Direction', pm.Vec3, CR.getDirection, CR.setDirection )
            ]
        )
        self.attributes.append( pAttr )
    

class CollisionSphere( Base ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', CS )
        Base.__init__( self, *args, **kwargs )
        
        self.initArgs = [pm.Point3( 0 ), 0.5]
        
        pAttr = Attr( 'Collision Sphere' )
        pAttr.children.extend( 
            [
                Attr( 'Center', pm.Point3, CS.getCenter, CS.setCenter ),
                Attr( 'Radius', float, CS.getRadius, CS.setRadius )
            ]
        )
        self.attributes.append( pAttr )
        

class CollisionInvSphere( CollisionSphere ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', CIS )
        CollisionSphere.__init__( self, *args, **kwargs )
        

class CollisionTube( Base ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', CT )
        Base.__init__( self, *args, **kwargs )
        
        self.initArgs = [pm.Point3( 0, 0, 0 ), pm.Point3( 0, 0, 1 ),0.5]
        
        pAttr = Attr( 'Collision Tube' )
        pAttr.children.extend( 
            [
                Attr( 'Point A', pm.Point3, CT.getPointA, CT.setPointA ),
                Attr( 'Point B', pm.Point3, CT.getPointB, CT.setPointB ),
                Attr( 'Radius', float, CT.getRadius, CT.setRadius )
            ]
        )
        self.attributes.append( pAttr )