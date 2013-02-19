import pandac.PandaModules as pm
from pandac.PandaModules import CollisionNode as CN, CollisionSolid as CS

from nodePath import NodePath
from attributes import NodeAttribute as Attr
from game.nodes.connections import NodePathSourceConnectionList as Cnnctn


class CollisionNode( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', CN )
        NodePath.__init__( self, *args, **kwargs )
        
        pAttr = Attr( 'CollisionNode' )
        pAttr.children.extend( 
            [
                Attr( 'Num Solids', int, CN.getNumSolids ),
                Cnnctn( 'Solids', CS, CN.getSolids, CN.addSolid, CN.clearSolids, self.RemoveSolid, self.data )
            ]
        )
        self.attributes.append( pAttr )
        
    def Create( self, *args, **kwargs ):
        np = NodePath.Create( self, *args, **kwargs )
        np.show()
        return np
    
    def RemoveSolid( self, srcComp, tgtComp ):
        solids = srcComp.getSolids()
        index = solids.index( tgtComp )
        CN.removeSolid( srcComp, index )