import wx
from wx.lib.pubsub import Publisher as pub

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
        tell the app to select those node paths.
        """
        # Bail if we got here by setting the item inside the OnUpdateSelection
        # method, we get stuck in an infinite loop otherwise.
        if self._updating:
            return
        
        # Set selected items
        items = self.GetValidSelections()
        if items:
            comps = [item.GetData() for item in items]
            cmds.Select( comps )
            
    def OnUpdate( self, msg ):
        """
        Select those items which correlate to the selected node paths. As long
        as our __nps dictionary is kept up to date we shouldn't have to
        iterate through the entire tree to find the items we need.
        """
        SceneGraphBasePanel.OnUpdate( self, msg )
        
        items = [
            self._comps[wrpr.data] 
            for wrpr in base.selection.wrprs 
            if wrpr.data in self._comps
        ]
        self.SelectItems( items )