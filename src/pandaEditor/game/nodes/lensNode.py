import pandac.PandaModules as pm
from pandac.PandaModules import Lens

from nodePath import NodePath
from attributes import Attribute as Attr


class LensNode( NodePath ):
    
    type_ = pm.LensNode
    
    def __init__( self, *args, **kwargs ):
        NodePath.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Fov', pm.Vec2, Lens.getFov, Lens.setFov, self.GetLens ),
            parent='LensNode'
        )
        
    def GetLens( self, np ):
        return np.node().getLens()