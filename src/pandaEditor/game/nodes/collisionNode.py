import pandac.PandaModules as pm
from pandac.PandaModules import CollisionNode as CN, CollisionSolid as CS

from nodePath import NodePath
from attributes import NodeAttribute as Attr
from game.nodes.attributes import NodePathSourceConnectionList as Cnnctn


class CollisionNode( NodePath ):
    
    type_ = CN
    
    def __init__( self, *args, **kwargs ):
        NodePath.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Num Solids', int, CN.getNumSolids ),
            Cnnctn( 'Solids', CS, CN.getSolids, CN.addSolid, CN.clearSolids, self.RemoveSolid, self.data ),
            parent='CollisionNode'
        )
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = super( CollisionNode, cls ).Create( *args, **kwargs )
        wrpr.data.show()
        return wrpr
    
    def RemoveSolid( self, srcComp, tgtComp ):
        solids = srcComp.getSolids()
        index = solids.index( tgtComp )
        CN.removeSolid( srcComp, index )