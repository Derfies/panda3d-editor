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
    initArgs = [pm.Point3( 0 ), 0.5]
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Center', pm.Point3, CB.getCenter, CB.setCenter ),
            parent='CollisionBox'
        )
    

class CollisionRay( Base ):
    
    type_ = CR
    initArgs = [pm.Point3( 0, 0, 0 ), pm.Vec3( 0, 0, 1 )]
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Origin', pm.Point3, CR.getOrigin, CR.setOrigin ),
            Attr( 'Direction', pm.Vec3, CR.getDirection, CR.setDirection ),
            parent='CollisionRay'
        )
    

class CollisionSphere( Base ):
    
    type_ = CS
    initArgs = [pm.Point3( 0 ), 0.5]
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Center', pm.Point3, CS.getCenter, CS.setCenter ),
            Attr( 'Radius', float, CS.getRadius, CS.setRadius ),
            parent='CollisionSphere'
        )
        

class CollisionInvSphere( CollisionSphere ):
    
    type_ = CIS
        

class CollisionTube( Base ):
    
    type_ = CT
    initArgs = [pm.Point3( 0, 0, 0 ), pm.Point3( 0, 0, 1 ),0.5]
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Point A', pm.Point3, CT.getPointA, CT.setPointA ),
            Attr( 'Point B', pm.Point3, CT.getPointB, CT.setPointB ),
            Attr( 'Radius', float, CT.getRadius, CT.setRadius ),
            parent='CollisionTube'
        )