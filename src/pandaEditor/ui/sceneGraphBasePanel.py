import wx
import pandac.PandaModules as pm
import wx.lib.agw.flatmenu as fm
import wx.lib.agw.fmresources as fmr
import wx.lib.agw.customtreectrl as ct
from wx.lib.pubsub import pub

import p3d
from .. import commands as cmds
from customDropTarget import CustomDropTarget
from wxExtra import utils as wxUtils
from wxExtra import CustomTreeCtrl, CompositeDropTarget


DISPLAY_NODEPATHS = wx.NewId()


class SceneGraphBasePanel( wx.Panel ):
    
    def __init__( self, *args, **kwargs ):
        wx.Panel.__init__( self, *args, **kwargs )
        
        self._comps = {}
        self.app = wx.GetApp()
        self.filter = pm.PandaNode
        
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
        self.dt = CustomDropTarget( ['filePath', 'nodePath'], self )
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
        
        # If the item under the middle mouse click is part of the selection
        # then use the whole selection, otherwise just use the item.
        if item.GetData() in self.app.selection.comps:
            dragComps = self.app.selection.comps
        else:
            dragComps = [item.GetData()]
        self.app.dDropMgr.Start( self, dragComps, item.GetData() )
        
    def GetDroppedObject( self, x, y ):
        dropItem = self.tc.HitTest( wx.Point( x, y ) )[0]
        if dropItem is None:
            return None
        else:
            return dropItem.GetData()
        
    def AddItem( self, wrpr, pItem ):
        """
        Traverse the scene from the root node, creating tree items for each
        component encountered.
        """
        # Bail if there is a filter set and the node is not derived from
        # that type.
        if self.filter is not None and not wrpr.IsOfType( self.filter ):
            return
            
        item = self.tc.AppendItem( pItem, wrpr.GetName(), data=wrpr.data )
        self._comps[wrpr.data] = item
        
        for cWrpr in wrpr.GetChildren():
            self.AddItem( cWrpr, item )
            
    def RemoveItem( self, wrpr, delete=True ):
        if wrpr.data in self._comps:
            if delete:
                self.tc.Delete( self._comps[wrpr.data] )
            del self._comps[wrpr.data]
            
        for cWrpr in wrpr.GetChildren():
            self.RemoveItem( cWrpr, False )
            
    def RefreshItem( self, wrpr ):
        pWrpr = wrpr.GetParent()
        if pWrpr is None:
            return
        
        if pWrpr.data in self._comps:
            newItem = self.tc.SetItemParent( self._comps[wrpr.data], 
                                             self._comps[pWrpr.data], 
                                             wrpr.GetSiblingIndex() )
            self.tc.SetItemText( newItem, wrpr.GetName() )
            self.UpdateItemData( newItem )
            
    def UpdateItemData( self, item ):
        data = self.tc.GetPyData( item )
        self._comps[data] = item
            
        for cItem in self.tc.GetItemChildren( item ):
            self.UpdateItemData( cItem )
        
    def OnUpdate( self, comps=None ):
        """
        Update the contents of the TreeCtrl to reflect the contents of the 
        scene. If comps is not None, it will contain only the components
        which have changed. This means we don't have to do a full rebuild of
        the tree which can be time consuming.
        """
        # No need to refresh a panel if it is hidden.
        if not self.IsShownOnScreen():
            return
        
        if comps is None:
            
            # No components were specified - do a full rebuild.
            self.Rebuild()
        else:
            for comp in comps:
                wrpr = base.game.nodeMgr.Wrap( comp )
                pWrpr = wrpr.GetParent()
                if wrpr.data in self._comps:
                    if pWrpr is None and wrpr.data != base.scene:
                        
                        # Component has no parent - remove it.
                        self.RemoveItem( wrpr )
                    else:
                        
                        # Component found in the tree - refresh it.
                        self.RefreshItem( wrpr )
                elif pWrpr.data in self._comps:
                    
                    # Component not found in the tree - add it.
                    self.AddItem( wrpr, self._comps[pWrpr.data] )
    
    def Rebuild( self ):
        """Do a complete rebuild of the scene graph."""
        # Get map of node paths to items before populating the tree control
        oldItems = self.GetItemsDictionary()

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
        newItems = self.GetItemsDictionary()
        self.SetExpandedState( oldItems, newItems )
        
    def GetItemsDictionary( self ):
        """
        Return a dictionary mapping the scene's components to the item that
        represents them in the tree.
        """
        expDict = {}
        for item in self.tc.GetItemChildren( self.tc.GetRootItem() ):
            expDict[item.GetData()] = item
        return expDict
    
    def SetExpandedState( self, oldItems, newItems ):
        """Set item expanded states back."""
        for comp, oldItem in oldItems.items():
            if comp in newItems and oldItem.IsExpanded():
                newItem = newItems[comp]
                if newItem == self.tc.GetRootItem():
                    continue
                self.tc.Expand( newItem )
        
    def SelectItems( self, items ):
        """
        Iterate over list and hilight them. Make sure the TreeCtrl is open at 
        the last item the user selected.
        """
        self.tc.UnselectAll()
        for item in items:
            item.SetHilight()
            
        if items:
            self.tc.CalculatePositions() 
            self.tc.EnsureVisible( items[-1] )
        
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