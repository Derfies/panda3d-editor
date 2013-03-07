from panda3d.bullet import BulletRigidBodyNode as BRBN

from game.nodes.attributes import NodeAttribute as Attr
from game.nodes.bulletRigidBodyNode import BulletRigidBodyNode as GameBulletRigidBodyNode


class BulletRigidBodyNode( GameBulletRigidBodyNode ):
    
    def __init__( self, *args, **kwargs ):
        GameBulletRigidBodyNode.__init__( self, *args, **kwargs )
        
        i = self.attributes.index( self.FindProperty( 'shapes' ) )
        self.AddAttributes( Attr( 'Num Shapes', int, BRBN.getNumShapes, w=False ), index=i )
        self.AddAttributes( Attr( 'Debug Enabled', bool, BRBN.isDebugEnabled, BRBN.setDebugEnabled, w=False ) )