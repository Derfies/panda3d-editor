import pandac.PandaModules as pm
from pandac.PandaModules import CollisionNode as CN

from nodePath import NodePath
from attributes import NodeAttribute as Attr


class CollisionNode( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', CN )
        NodePath.__init__( self, *args, **kwargs )
        
        pAttr = Attr( 'CollisionNode' )
        pAttr.children.extend( 
            [
                Attr( 'Num Solids', int, CN.getNumSolids )
            ]
        )
        self.attributes.append( pAttr )