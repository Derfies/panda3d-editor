import wx
import pandac.PandaModules as pm
import wx.lib.agw.flatmenu as fm
import wx.lib.agw.fmresources as fmr
import wx.lib.agw.customtreectrl as ct
from wx.lib.pubsub import Publisher as pub

import p3d
from .. import commands as cmds
from wxExtra import utils as wxUtils
from wxExtra import CustomTreeCtrl, CompositeDropTarget


DISPLAY_NODEPATHS = wx.NewId()


class SceneGraphBasePanel( wx.Panel ):
    
    def __init__( self, *args, **kwargs ):
        wx.Panel.__init__( self, *args, **kwargs )
        
        self.app = wx.GetApp()
        self.filter = pm.PandaNode
        self._updating = False
        self.dragComps = []
        
        # Build display filter menu.
        fileMenu = fm.FlatMenu()
        item = fm.FlatMenuItem( fileMenu, DISPLAY_NODEPATHS, '&NodePaths Only', '', wx.ITEM_CHECK )
        item.Check()
        fileMenu.AppendItem( item )
        
        self.fm = fm.FlatMenuBar( self, -1, 16, 1, options=fmr.FM_OPT_IS_LCD )
        self.fm.Append( fileMenu, '&Display' )
        self.fm.GetRendererManager().SetTheme( fm.StyleVista )
        
        ln = wx.StaticLine( self, -1, style=wx.LI_HORIZONTAL )
        
        # Bind menu controls
        self.Bind( fm.EVT_FLAT_MENU_SELECTED, self.OnFlatMenuSelected, id=DISPLAY_NODEPATHS )
        
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
        self.tc.Bind( wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnTreeBeginLabelEdit )
        self.tc.Bind( wx.EVT_TREE_END_LABEL_EDIT, self.OnTreeEndLabelEdit )
        self.tc.Bind( wx.EVT_LEFT_DCLICK, self.OnLeftDClick )
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
        self.bs1.Add( self.fm, 0, wx.EXPAND )
        self.bs1.Add( ln, 0, wx.EXPAND )
        self.bs1.Add( self.tc, 1, wx.EXPAND )
        self.SetSizer( self.bs1 )
        
    def OnFlatMenuSelected( self, evt ):
        
        # Set the filter based on the flat menu selection.
        self.filter = None
        val = self.fm.FindMenuItem( DISPLAY_NODEPATHS ).IsChecked()
        if val:
            self.filter = pm.PandaNode
            
        self.app.doc.OnRefresh()
        
    def OnTreeBeginLabelEdit( self, evt ):
        """
        Highlight the text of the tree item label as soon as the edit process
        has started. This must be done with CallAfter otherwise GetEditControl
        will return None.
        """
        def HighlightText( tc ):
            ctrl = tc.GetEditControl()
            ctrl.SetSelection( -1, -1 )
            
        wx.CallAfter( HighlightText, self.tc )
            
    def OnTreeEndLabelEdit( self, evt ):
        """Change the component's name to that of the new item's name."""
        def SetComponentName( comp, name ):
            wrpr = base.game.nodeMgr.Wrap( comp )
            attr = wrpr.FindProperty( 'name' )
            if attr is not None:
                wx.CallAfter( cmds.SetAttribute, [comp], [attr], name )
        
        comp = evt.GetItem().GetData()
        name = evt.GetLabel()
        if not name:
            return
        wx.CallAfter( SetComponentName, comp, name )
        
    def OnLeftDClick( self, evt ):
        item = wxUtils.GetClickedItem( self.tc, evt )
        if item is not None:
            self.tc.EditLabel( item )
            
    def OnMiddleDown( self, evt ):
        
        # Get the item under the mouse - bail if the item is bad
        item = wxUtils.GetClickedItem( self.tc, evt )
        if item is None or not item.IsOk():
            return
        
        # Create a custom data object that we can drop onto the toolbar
        # which contains the tool's id as a string
        do = wx.CustomDataObject( 'NodePath' )
        do.SetData( str( item.GetData() ) )
        
        # If the item under the middle mouse click is part of the selection
        # then use the whole selection, otherwise just use the item.
        if item.GetData() in self.app.selection.comps:
            self.dragComps = self.app.selection.comps
        else:
            self.dragComps = [item.GetData()]
        
        # Create the drop source and begin the drag and drop operation
        ds = wx.DropSource( self )
        ds.SetData( do )
        ds.DoDragDrop( wx.Drag_AllowMove )
        
        # Clear drag node paths
        self.dragComps = []
            
    def ValidateDropItem( self, x, y ):
        """Perform validation procedures."""
        dropItem = self.tc.HitTest( wx.Point( x, y ) )[0]
        if dropItem is None:
            return False
        
        wrpr = base.game.nodeMgr.Wrap( dropItem.GetData() )
        if wx.GetMouseState().CmdDown():
            return wrpr.ValidateDragDrop( self.dragComps, dropItem.GetData() )
        else:
            return wrpr.GetPossibleConnections( self.dragComps )
            
    def OnDropItem( self, str ):
        
        # Get the item at the drop point
        dropItem = self.tc.HitTest( wx.Point( self.dt.x, self.dt.y ) )[0]
        wrpr = base.game.nodeMgr.Wrap( dropItem.GetData() )
        self.data = {}
        if wx.GetMouseState().CmdDown():
            wrpr.OnDragDrop( self.dragComps, wrpr.data )
        else:
            menu = wx.Menu()
            for cnnctn in wrpr.GetPossibleConnections( self.dragComps ):
                mItem = wx.MenuItem( menu, wx.NewId(), cnnctn.label )
                menu.AppendItem( mItem )
                self.Bind( wx.EVT_MENU, self.OnConnect, id=mItem.GetId() )
                self.data[mItem.GetId()] = cnnctn
            self.PopupMenu( menu )
            menu.Destroy()
        
    def OnConnect( self, evt ):
        menu = evt.GetEventObject()
        mItem = menu.FindItemById( evt.GetId() )
        cnnctn = self.data[evt.GetId()]
        cmds.Connect( self.dragComps, cnnctn, cnnctn.Connect )
        
    def AddItem( self, wrpr, pItem ):
        """
        Traverse the scene from the root node, creating tree items for each
        node path encountered.
        """
        # Bail if there is a filter set and the node is not derived from
        # that type.
        if self.filter is not None and not wrpr.IsOfType( self.filter ):
            return
            
        item = self.tc.AppendItem( pItem, wrpr.GetName() )
        item.SetData( wrpr.data )
        self._comps[wrpr.data] = item
        
        for cWrpr in wrpr.GetChildren():
            self.AddItem( cWrpr, item )
        
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
        self._comps = {}
        rItem = self.tc.AddRoot( 'root' )
        wrpr = base.game.nodeMgr.Wrap( base.scene )
        if self.filter is None:
            self.AddItem( wrpr, rItem )
        else:
            for cWrpr in wrpr.GetChildren(): 
                self.AddItem( cWrpr, rItem )
            
        # Get map of node paths to items after populating the tree control
        newItems = GetItemsDict()
        
        # Set item states back
        sels = []
        for np, oldItem in oldItems.items():
            
            # Set expanded states back
            if np in newItems and oldItem.IsExpanded():
                self.tc.Expand( newItems[np] )
            
            # Set selection states back
            #if np in newItems and oldItem.IsSelected():
            #    self.tc.SelectItem( newItems[np] )
                
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
        
    def GetValidSelections( self ):
        """
        Return a list of selected items, making sure that they are valid by
        using IsOk() and are not the root item.
        """
        items = []
        
        for item in self.tc.GetSelections():
            if item.IsOk() and item is not self.tc.GetRootItem():
                items.append( item )
                
        return items