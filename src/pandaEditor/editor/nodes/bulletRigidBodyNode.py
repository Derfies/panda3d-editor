from panda3d.bullet import BulletShape, BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode as BRBN

from constants import *
from game.nodes.attributes import NodeAttribute as Attr
from game.nodes.bulletRigidBodyNode import BulletRigidBodyNode as GameBulletRigidBodyNode


BULLET_SHAPES = [
    BulletBoxShape
]


class BulletRigidBodyNode( GameBulletRigidBodyNode ):
    
    def __init__( self, *args, **kwargs ):
        GameBulletRigidBodyNode.__init__( self, *args, **kwargs )
        
        pAttr = self.FindProperty( 'bulletRigidBodyNode' )
        pAttr.children.extend( 
            [
                Attr( 'Num Shapes', int, BRBN.getNumShapes, w=False ),
                Attr( 'Debug Enabled', bool, BRBN.isDebugEnabled, BRBN.setDebugEnabled, w=False )
            ]
        )
        
    def GetConnections( self ):
        data = {}
        
        shapes = self.data.node().getShapes()
        if shapes:
            data['shape'] = []
            for shape in shapes:
                if shape in base.scene.comps:
                    uuid = base.scene.comps[shape]
                    data['shape'].append( uuid )
        return data