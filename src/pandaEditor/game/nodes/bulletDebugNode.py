import pandac.PandaModules as pm
from panda3d.bullet import BulletDebugNode as BDN

from .nodePath import NodePath
from .attributes import NodePathAttribute as Attr


TAG_BULLET_DEBUG_WIREFRAME = 'P3D_BulletDebugWireframe'


class BulletDebugNode( NodePath ):
    
    type_ = BDN
    
    def __init__( self, *args, **kwargs ):
        NodePath.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Show Wireframe', bool, self.GetWireframe, self.SetWireframe ),
            parent='BulletDebugNode'
        )
        
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = super( BulletDebugNode, cls ).Create( *args, **kwargs )
        wrpr.SetWireframe( wrpr.data, True )
        wrpr.data.show()
        return wrpr
        
    def GetWireframe( self, np ):
        return np.getPythonTag( TAG_BULLET_DEBUG_WIREFRAME )
    
    def SetWireframe( self, np, val ):
        np.node().showWireframe( val )
        np.setPythonTag( TAG_BULLET_DEBUG_WIREFRAME, val )
