import pandac.PandaModules as pm

from p3d import commonUtils as utils
import game
from .constants import *
from game.nodes.nodePath import NodePath
from game.nodes.collisionNode import CollisionNode


class EmbeddedCollision( CollisionNode ):
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        #wrpr = super( Actor, cls ).Create( *args, **kwargs )
        
        
        
        
        
        
        
        
        if 'inputNp' in kwargs:
            np = kwargs['inputNp']
            
        #print np
        #print np.node()
        #print 'find: ', np.findAllMatches('**/+GeomNode')
        #print 'find: ', np.findAllMatches('**+GeomNode')
        #print 'find: ', np.findAllMatches('**/*+GeomNode')
        #print 'find: ', np.findAllMatches('/**+GeomNode')
        
        collNps = np.findAllMatches('**/+GeomNode')
        collNps.addPath( np )
        newCollNp = utils.RebuildGeomNodesToColPolys( collNps ).getChildren()[0]
        newCollNp.show()
        
        newCollNp.reparentTo( np.getParent() )
        newCollNp.setName( 'NEW NODE' )
        newCollNp.show()
        newCollNp.setTag( game.nodes.TAG_NODE_TYPE, TAG_EMBEDDED_COLLISION )
        np.detachNode()
        
        wrpr = cls( newCollNp )
        wrpr.SetupNodePath()
        #for t in wrpr.attributes:
        #    print t.label
        return wrpr