import pandac.PandaModules as pm
from pandac.PandaModules import Light as L

from nodePath import NodePath
from attributes import NodeAttribute as Attr


class Light( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        NodePath.__init__( self, *args, **kwargs )
        
        self.attributes.extend( 
            [
                Attr( 'Color', pm.Vec4, L.getColor, L.setColor )
            ]
        )
    
    def Create( self ):
        np = NodePath.Create( self )
        
        # DEBUG
        render.setLight( np )
        
        return np