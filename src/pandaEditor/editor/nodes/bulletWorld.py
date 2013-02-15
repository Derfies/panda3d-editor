import panda3d.bullet as bllt
import pandac.PandaModules as pm
from panda3d.bullet import BulletWorld as BW

from game.nodes.constants import *
from pandaEditor import commands as cmds
from game.nodes.attributes import Attribute as Attr
from game.nodes.bulletWorld import BulletWorld as GameBulletWorld


BULLET_TYPES = [
    bllt.BulletRigidBodyNode
]


class BulletWorld( GameBulletWorld ):
    
    def __init__( self, *args, **kwargs ):
        GameBulletWorld.__init__( self, *args, **kwargs )
        
        pAttr = self.FindProperty( 'bulletWorld' )
        pAttr.children.extend( 
            [
                Attr( 'Num Rigid Bodies', int, BW.getNumRigidBodies, w=False )
            ]
        )
            
    def GetConnections( self ):
        data = {}
        
        rigidBodies = self.data.getRigidBodies()
        if rigidBodies:
            data['rigidBody'] = []
            for rigidBody in rigidBodies:
                uuid = pm.NodePath( rigidBody ).getTag( TAG_NODE_UUID )
                data['rigidBody'].append( uuid )
        
        return data