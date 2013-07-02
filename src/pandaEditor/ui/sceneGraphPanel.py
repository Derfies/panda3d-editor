import wx

from .. import commands as cmds
from sceneGraphBasePanel import SceneGraphBasePanel


class SceneGraphPanel( SceneGraphBasePanel ):
    
    def __init__( self, *args, **kwargs ):
        SceneGraphBasePanel.__init__( self, *args, **kwargs )
        
        # Bind tree control events
        self.tc.Bind( wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelChanged )
        
    def OnTreeSelChanged( self, evt ):
        """
        Tree item selection handler. If the selection of the tree changes,
        tell the app to select those components.
        """
        def IndexInSelection( x, comps ):
            """
            Sort components by their position in the selection, if they appear
            there. This will make the new selection order closer to the 
            original.
            """
            if x in base.selection.comps:
                i = base.selection.comps.index( x )
            else:
                i = len(  base.selection.comps )
            return i
            
        items = self.GetValidSelections()
        if items:
            comps = [item.GetData() for item in items]
            comps.sort( key=lambda x: IndexInSelection( x, comps ) )
            cmds.Select( comps )
            
    def OnUpdate( self, msg ):
        """
        Update the TreeCtrl then hilight those items whose components are 
        selected.
        """
        self.tc.Freeze()
        
        SceneGraphBasePanel.OnUpdate( self, msg )
        items = [
            self._comps[comp] 
            for comp in base.selection.comps 
            if comp in self._comps
        ]
        self.SelectItems( items )
        
        self.tc.Thaw()