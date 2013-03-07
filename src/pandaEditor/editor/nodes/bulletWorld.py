from panda3d.bullet import BulletWorld as BW

from game.nodes.attributes import Attribute as Attr
from game.nodes.attributes import Connection as Cnnctn
from game.nodes.bulletWorld import BulletWorld as GameBulletWorld


class BulletWorld( GameBulletWorld ):
    
    def __init__( self, *args, **kwargs ):
        GameBulletWorld.__init__( self, *args, **kwargs )
        
        i = self.attributes.index( self.FindProperty( 'rigidBody' ) )
        self.AddAttributes( Attr( 'Num Rigid Bodies', int, BW.getNumRigidBodies, w=False ), index=i )
    
    def SetDefaultValues( self ):
        GameBulletWorld.SetDefaultValues( self )
        
        # Set this world as the default physics world if one has not already
        # been set.
        if base.scene.physicsWorld is None:
            cnnctn = Cnnctn( 'PhysicsWorld', None, base.scene.GetPhysicsWorld, base.scene.SetPhysicsWorld, base.scene.ClearPhysicsWorld, srcComp=base.scene )
            cnnctn.Connect( self.data )