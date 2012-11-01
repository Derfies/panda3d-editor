from constants import *
from game.nodes.nodePath import NodePath as GameNodePath


class NodePath( GameNodePath ):
    
    geo = None
    pickable = True
        
    @classmethod
    def SetPickable( cls, value=True ):
        cls.pickable = value
        
    @classmethod
    def SetEditorGeometry( cls, geo ):
        geo.setPythonTag( TAG_IGNORE, True )
        geo.setLightOff()
        geo.node().adjustDrawMask( *base.GetEditorRenderMasks() )
        cls.geo = geo
        
    def SetupNodePath( self, np ):
        GameNodePath.SetupNodePath( self, np )
        
        if self.geo is not None:
            self.geo.copyTo( np )
            
        if self.pickable:
            np.setPythonTag( TAG_PICKABLE, self.pickable )
            
    def OnSelect( self, np ):
        pass
    
    def OnDeselect( self, np ):
        pass