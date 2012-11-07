import wx
import wx.lib.agw.customtreectrl as ct
from wx.lib.pubsub import Publisher as pub

import p3d
from .. import commands as cmds
from wxExtra import CustomTreeCtrl, CompositeDropTarget


class SceneGraphBasePanel( wx.Panel ):
    
    def __init__( self, *args, **kwargs ):
        wx.Panel.__init__( self, *args, **kwargs )
        
        self._updating = False
        self._selUpdating = False
        self.dragNps = []
        
        # Build tree control
        self.tc = CustomTreeCtrl( self, -1, agwStyle=
                                  ct.TR_EDIT_LABELS |
                                  ct.TR_HIDE_ROOT | 
                                  ct.TR_FULL_ROW_HIGHLIGHT |
                                  ct.TR_NO_LINES |
                                  ct.TR_HAS_BUTTONS |
                                  ct.TR_TWIST_BUTTONS |
                                  ct.TR_MULTIPLE )
        self.tc.AddRoot( 'root' )
        
        # Bind tree control events
        self.tc.Bind( wx.EVT_TREE_END_LABEL_EDIT, self.OnTreeEndLabelEdit )
        self.tc.Bind( wx.EVT_TREE_ITEM_ACTIVATED, self.OnTreeItemActivated )
        self.tc.Bind( wx.EVT_KEY_UP, p3d.wx.OnKeyUp )
        self.tc.Bind( wx.EVT_KEY_DOWN, p3d.wx.OnKeyDown )
        self.tc.Bind( wx.EVT_LEFT_UP, p3d.wx.OnLeftUp )
        self.tc.Bind( wx.EVT_MIDDLE_DOWN, self.OnMiddleDown )
        
        # Build tree control drop target
        self.dt = CompositeDropTarget( ['filePath', 'nodePath'], 
                                       self.OnDropItem, 
                                       self.ValidateDropItem )
        self.tc.SetDropTarget( self.dt )
                
        # Bind publisher events
        pub.subscribe( self.OnUpdate, 'Update' )
        
        # Build sizers
        self.bs1 = wx.BoxSizer( wx.VERTICAL )
        self.bs1.Add( self.tc, 1, wx.EXPAND )
        self.SetSizer( self.bs1 )
            
    def OnTreeEndLabelEdit( self, evt ):
        """Match the node path's name to the new name of the item."""
        def setNodePathName( np, name ):
            np.setName( name )
            wx.CallAfter( wx.GetApp().doc.OnModified )
        np = evt.GetItem().GetData()
        name = evt.GetLabel()
        if not name:
            return
        wx.CallAfter( setNodePathName, np, name )
        
    def OnTreeItemActivated( self, evt ):
        """Put the event item into label edit mode."""
        self.tc.EditLabel( evt.GetItem() )
            
    def OnMiddleDown( self, evt ):
        
        # Get the item under the mouse - bail if the item is bad
        item = self.tc.HitTest( wx.Point( evt.GetX(), evt.GetY() ) )[0]
        if item is None or not item.IsOk():
            return
        
        # Create a custom data object that we can drop onto the toolbar
        # which contains the tool's id as a string
        do = wx.CustomDataObject( 'NodePath' )
        do.SetData( str( item.GetData() ) )
        
        # If the item under the middle mouse click is part of the selection
        # then use the whole selection, otherwise just use the item.
        if item.GetData() in wx.GetApp().selection.nps:
            self.dragNps = wx.GetApp().selection.nps
        else:
            self.dragNps = [item.GetData()]
        
        # Create the drop source and begin the drag and drop operation
        ds = wx.DropSource( self )
        ds.SetData( do )
        ds.DoDragDrop( wx.Drag_AllowMove )
        
        # Clear drag node paths
        self.dragNps = []
            
    def ValidateDropItem( self, x, y ):
        """Perform validation procedures."""
        dropItem = ( self.tc.HitTest( wx.Point( x, y ) ) )[0]
        
        # If the drop item is none then the drop item will default to the
        # root node. No other checks necessary.
        if dropItem is None:
            return True
            
        # Fail if the drop item is one of the items being dragged
        dropNp = dropItem.GetData()
        if dropNp in self.dragNps:
            return False
        
        # Fail if the drag items are ancestors of the drop items
        for np in self.dragNps:
            if np.isAncestorOf( dropNp ):
                return False
        
        # Drop target item is ok, continue
        return True
            
    def OnDropItem( self, str ):
        
        # Get the item at the drop point
        dropItem = ( self.tc.HitTest( wx.Point( self.dt.x, self.dt.y ) ) )[0]
        
        # Check if there are drag node paths set, if so perform parenting
        # operation
        if not self.dragNps:
            np = None
            if dropItem is not None:
                np = dropItem.GetData()
            wx.GetApp().AddFile( str, np )
            return
            
        # Get the parent
        if dropItem is not None and dropItem.IsOk():
            parentNp = dropItem.GetData()
        else:
            parentNp = wx.GetApp().doc.contents.rootNp
        
        # Parent all dragged node paths
        cmds.Parent( self.dragNps, parentNp )
            
    def PopulateTreeControl( self ):
        """
        Traverse the scene from the root node, creating tree items for each
        node path encountered.
        """
        def AddItem( np, parentItem ):
            if np is base.scene.rootNp:
                return
            if np.getParent() in self._nps:
                parentItem = self._nps[np.getParent()]
            else:
                parentItem = self.tc.GetRootItem()
            item = self.tc.AppendItem( parentItem, np.getName() )
            item.SetData( np )
            self._nps[np] = item
        
        # Clear the node path / tree item dict
        self._nps = {}
        
        # Create scene root node, then recurse down scene hierarchy
        self.tc.AddRoot( 'root' )
        wx.GetApp().doc.contents.Walk( AddItem, includeHelpers=False, modelRootsOnly=False )
        
    def OnUpdate( self, msg ):
        """
        Update the tree control by removing all items and replacing them.
        """
        self._updating = True
        self.tc.Freeze()
        
        def GetItemsDict():
            
            # Return a dictionary mapping each node path to its tree item.
            itemsDict = {}
            for item in self.tc.GetAllItems():
                itemsDict[item.GetData()] = item
            return itemsDict
        
        # Get map of node paths to items before populating the tree control
        oldItems = GetItemsDict()

        # Clear existing items and repopulate tree control
        self.tc.DeleteAllItems()
        self.PopulateTreeControl()
        
        # Get map of node paths to items after populating the tree control
        newItems = GetItemsDict()
        
        # Set item states back
        sels = []
        for np, oldItem in oldItems.items():
            
            # Set expanded states back
            if np in newItems and oldItem.IsExpanded():
                self.tc.Expand( newItems[np] )
            
            # Set selection states back
            if np in newItems and oldItem.IsSelected():
                self.tc.SelectItem( newItems[np] )
                
        self.tc.Thaw()
        self._updating = False
        
    def SelectItems( self, items, unselect=True ):
        """
        The tree control tries to redraw every time we call SelectItem() which
        can cause flickering (even when frozen!) when iterating through a 
        list. Disconnecting the event handler seems to stop the internal 
        redrawing, at least until we get a SelectItems() method.
        """
        self.Freeze()
        self.tc.SetEvtHandlerEnabled( False )
        
        # Deselect all if indicated
        if unselect:
            self.tc.UnselectAll()
            
        # Iterate over list and select
        for item in items:
            self.tc.SelectItem( item )
        
        # Make sure to call refresh at least once since we disabled the event
        # handler that would normally do this!
        self.tc.SetEvtHandlerEnabled( True )
        self.tc.Refresh()
        self.Thaw()