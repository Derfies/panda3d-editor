import wx
from wx.lib.pubsub import Publisher as pub

from .. import commands as cmds
from sceneGraphBasePanel import SceneGraphBasePanel


class SceneGraphPanel( SceneGraphBasePanel ):
    
    def __init__( self, *args, **kwargs ):
        SceneGraphBasePanel.__init__( self, *args, **kwargs )
        
        # Bind tree control events
        self.tc.Bind( wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelChanged )
        
        # Bind publisher events
        pub.subscribe( self.OnUpdateSelection, 'UpdateSelection' )
        
    def OnTreeSelChanged( self, evt ):
        """
        Tree item selection handler. If the selection of the tree changes,
        tell the app to select those node paths.
        """
        # Bail if we got here by setting the item inside the OnUpdateSelection
        # method, we get stuck in an infinite loop otherwise
        if self._selUpdating or self._updating:
            return
        
        # Get all valid selected items
        items = []
        for item in self.tc.GetSelections():
            if item.IsOk() and item is not self.tc.GetRootItem():
                items.append( item )
        
        # Set selected items
        if items:
            nps = [item.GetData() for item in items]
            cmds.Select( nps )
            
    """
            
    def OnUpdate( self, msg ):
        SceneGraphBasePanel.OnUpdate( self, msg )
        
        def GetItemsDict():
            
            # Return a dictionary mapping each node path to its tree item.
            itemsDict = {}
            for item in self.tc.GetAllItems():
                itemsDict[item.GetData()] = item
            return itemsDict
        
        # Set the selection back
        newItems = GetItemsDict()
        selItems = [
            newItems[np] for np in wx.GetApp().selection.nps
            if np in newItems
        ]
        self.SelectItems( selItems )
    """
            
    def OnUpdateSelection( self, msg ):
        """
        Select those items which correlate to the selected node paths. As long
        as our __nps dictionary is kept up to date we shouldn't have to
        iterate through the entire tree to find the items we need.
        """
        self._selUpdating = True

        items = [self._nps[np] for np in msg.data if np in self._nps]
        self.SelectItems( items )

        self._selUpdating = False