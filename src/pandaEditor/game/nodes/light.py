import pandac.PandaModules as pm
from pandac.PandaModules import Light as L

from .nodePath import NodePath
from .attributes import NodeAttribute as Attr


class Light( NodePath ):
    
    type_ = L
    
    def __init__( self, *args, **kwargs ):
        NodePath.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Color', pm.Vec4, L.getColor, L.setColor ),
            parent='Light'
        )