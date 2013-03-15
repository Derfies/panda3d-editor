import uuid

import panda3d.bullet as blt
import pandac.PandaModules as pm

import p3d
import game
from constants import *
from game.nodes.constants import *
from editor.nodes.constants import *
from game.nodes.nodePath import NodePath
from game.nodes.collisionNode import CollisionNode
from game.nodes.bulletRigidBodyNode import BulletRigidBodyNode


class EmbeddedBulletTriangleMeshShape( BulletRigidBodyNode ):
    
    def __init__( self, *args, **kwargs ):
        BulletRigidBodyNode.__init__( self, *args, **kwargs )
        
        # Remove the shapes connection as this is built from the input 
        # NodePath.
        #self.attributes.
        cnnctn = self.FindProperty( 'shapes' )
        self.attributes.remove( cnnctn )
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        print '**CREATE METHOD***'
        if 'inputNp' in kwargs:
            inputNp = kwargs['inputNp']
            print 'using: ', inputNp
        elif 'path' in kwargs:
            #print 'pathed'
            inputNp = cls( cls.FindChild( kwargs['path'], kwargs['parent'] ) )
            print 'using: ', inputNp.data
            return inputNp
        
        # Get all geom nodes at this level and below.
        #geomNps = inputNp.findAllMatches( '**/+GeomNode' )
        #if inputNp.node().isOfType( pm.GeomNode ):
        #    geomNps.addPath( inputNp )
        
        geomNps = [inputNp]
            
        # Get a flat list of all geoms.
        geoms = []
        for geomNp in geomNps:
            geoms.extend( geomNp.node().getGeoms() )
            
        mesh = blt.BulletTriangleMesh()
        for geom in geoms:
            mesh.addGeom( geom )
            
        shape = blt.BulletTriangleMeshShape( mesh, dynamic=False )
        rBody = blt.BulletRigidBodyNode( inputNp.getName() )
        rBody.addShape( shape )
        
        # Swap the original NodePath for the one we just created.
        np = pm.NodePath( rBody )
        np.reparentTo( inputNp.getParent() )
        np.setTag( game.nodes.TAG_NODE_TYPE, TAG_EMBEDDED_BULLET_TRIANGLE_MESH_SHAPE )
        
        inputNp.detachNode()
        wrpr = cls( np )
        id = str( uuid.uuid4() )
        wrpr.data.setTag( TAG_NODE_UUID, id )
        np.setPythonTag( TAG_MODIFIED, True )
        
        return wrpr