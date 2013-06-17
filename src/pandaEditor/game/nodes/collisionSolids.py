import pandac.PandaModules as pm
from pandac.PandaModules import CollisionBox as CB
from pandac.PandaModules import CollisionRay as CR
from pandac.PandaModules import CollisionSphere as CS
from pandac.PandaModules import CollisionInvSphere  as CIS
from pandac.PandaModules import CollisionTube as CT

from base import Base
from attributes import Attribute as Attr


class CollisionBox( Base ):
    
    type_ = CB
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'X', float, initDefault=0.5 ),
            Attr( 'Y', float, initDefault=0.5 ),
            Attr( 'Z', float, initDefault=0.5 ),
            Attr( 'Center', pm.Point3, CB.getCenter, CB.setCenter, 
                  initDefault=pm.Point3( 0 ) ),
            parent='CollisionBox'
        )
    

class CollisionRay( Base ):
    
    type_ = CR
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Origin', pm.Point3, CR.getOrigin, CR.setOrigin, 
                  initDefault=pm.Point3( 0 ) ),
            Attr( 'Direction', pm.Vec3, CR.getDirection, CR.setDirection,
                  initDefault=pm.Vec3( 0, 0, 1 ) ),
            parent='CollisionRay'
        )
    

class CollisionSphere( Base ):
    
    type_ = CS
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Center', pm.Point3, CS.getCenter, CS.setCenter, 
                  initDefault=pm.Point3( 0 ) ),
            Attr( 'Radius', float, CS.getRadius, CS.setRadius,
                  initDefault=0.5 ),
            parent='CollisionSphere'
        )
        

class CollisionInvSphere( CollisionSphere ):
    
    type_ = CIS
        

class CollisionTube( Base ):
    
    type_ = CT
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Point A', pm.Point3, CT.getPointA, CT.setPointA, 
                  initDefault=pm.Point3( 0 ), initName='a' ),
            Attr( 'Point B', pm.Point3, CT.getPointB, CT.setPointB, 
                  initDefault=pm.Point3( 0, 0, 1 ), initName='db' ),
            Attr( 'Radius', float, CT.getRadius, CT.setRadius, 
                  initDefault=0.5 ),
            parent='CollisionTube'
        )