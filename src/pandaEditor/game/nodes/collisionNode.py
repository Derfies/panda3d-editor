import pandac.PandaModules as pm
from pandac.PandaModules import CollisionNode as CN

from nodePath import NodePath
from attributes import NodeAttribute as Attr


class CollisionNode( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        kwargs['nType'] = CN
        NodePath.__init__( self, *args, **kwargs )
        
        self.attributes.extend( 
            [
                Attr( 'Num Solids', int, CN.getNumSolids )
            ]
        )