import pandac.PandaModules as pm
from panda3d.bullet import BulletWorld as BW
from panda3d.bullet import BulletRigidBodyNode as BRBN

from base import Base
from attributes import Attribute as Attr
from game.nodes.connections import NodePathTargetConnectionList as Cnnctn


class BulletWorld( Base ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', BW )
        Base.__init__( self, *args, **kwargs )
        
        pAttr = Attr( 'BulletWorld' )
        pAttr.children.extend( 
            [
                Attr( 'Gravity', pm.Vec3, BW.getGravity, BW.setGravity ),
                Cnnctn( 'Rigid Body', BRBN, BW.getRigidBodies, BW.attachRigidBody, self.ClearRigidBodies, BW.removeRigidBody, self.data )
            ]
        )
        self.attributes.append( pAttr )
        
    def ClearRigidBodies( self, comp ):
        numRigidBodies = comp.getNumRigidBodies()
        for i in range( numRigidBodies ):
            rBody = comp.getRigidBody( 0 )
            comp.removeRigidBody( rBody )