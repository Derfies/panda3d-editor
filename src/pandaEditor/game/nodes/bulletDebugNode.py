import pandac.PandaModules as pm
from panda3d.bullet import BulletDebugNode as BDN

from nodePath import NodePath
from attributes import NodePathAttribute as Attr


TAG_BULLET_DEBUG_WIREFRAME = 'P3D_BulletDebugWireframe'


class BulletDebugNode( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', BDN )
        NodePath.__init__( self, *args, **kwargs )
        
        pAttr = Attr( 'BulletDebugNode' )
        pAttr.children.extend( 
            [
                Attr( 'Show Wireframe', bool, self.GetWireframe, self.SetWireframe )
            ]
        )
        self.attributes.append( pAttr )
        
    def Create( self, *args, **kwargs ):
        np = NodePath.Create( self, *args, **kwargs )
        self.SetWireframe( np, True )
        np.show()
        return np
        
    def GetWireframe( self, np ):
        return np.getPythonTag( TAG_BULLET_DEBUG_WIREFRAME )
    
    def SetWireframe( self, np, val ):
        np.node().showWireframe( val )
        np.setPythonTag( TAG_BULLET_DEBUG_WIREFRAME, val )
