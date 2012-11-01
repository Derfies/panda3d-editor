import pandac.PandaModules as pm
from pandac.PandaModules import Lens

from nodePath import NodePath
from attributes import Attribute as Attr


class LensNode( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        kwargs['nType'] = pm.LensNode
        NodePath.__init__( self, *args, **kwargs )
        
        self.attributes.extend( 
            [
                Attr( 'Fov', pm.Vec2, Lens.getFov, Lens.setFov, self.GetLens )
            ]
        )
        
    def GetLens( self, np ):
        return np.node().getLens()