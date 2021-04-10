import wx
import wx.lib.agw.customtreectrl as ct


class CustomTreeCtrl( ct.CustomTreeCtrl ):
    
    def __init__( self, *args, **kwargs ):
        ct.CustomTreeCtrl.__init__( self, *args, **kwargs )
        
        self.SetBorderPen( wx.Pen( (0, 0, 0), 0, wx.TRANSPARENT ) )
        self.EnableSelectionGradient( True )
        self.SetGradientStyle( True )
        self.SetFirstGradientColour( wx.Colour(46, 46, 46) )
        self.SetSecondGradientColour( wx.Colour(123, 123, 123) )
    
    def GetItemChildren( self, pItem, recursively=False ):
        """
        wxPython's standard tree control does not have a get item children
        method by default.
        """
        cItems = []
        
        cItem, cookie = self.GetFirstChild( pItem )
        while cItem is not None and cItem.IsOk():
            cItems.append( cItem )
            if recursively:
                cItems.extend( self.GetItemChildren( cItem, True ) )
            cItem = self.GetNextSibling( cItem )
            
        return cItems
    
    def FindItemByText( self, text ):
        """
        Iterate through all items and return the first which matches the given
        text.
        """
        def Recurse( item, text ):
            for child in self.GetItemChildren( item ):
                if self.GetItemText( child ) == text:
                    return child
            
                Recurse( child, text )
            
        return Recurse( self.GetRootItem(), text )
    
    def GetAllItems( self ):
        """Return a list of all items in the control."""
        def GetChildren( item, allItems ):
            if item is None:
                return
            for child in self.GetItemChildren( item ):
                allItems.append( child )
                GetChildren( child, allItems )
        
        allItems = []
        GetChildren( self.GetRootItem(), allItems )
        return allItems
    
    def SetItemParent( self, item, pItem, index=None, delete=True ):
        """
        Set the indicated item to the indicated parent item. Since the 
        TreeCtrl has no native way to do this, we have to delete the item
        then recreate it and all its children from scratch.
        """
        if index is None:
            index = self.GetChildrenCount( pItem )
        newItem = self.InsertItem( pItem, index, self.GetItemText( item ) )
        
        # Rebuild all decendants.
        for cItem in self.GetItemChildren( item ):
            self.SetItemParent( cItem, newItem, delete=False )
        
        # Set new items properties to match the old items properties.
        #self.SetItemData( newItem, self.GetItemData( item ) )
        newItem.SetData( item.GetData() )
        if item.IsExpanded():
            newItem.Expand()
        if item.IsSelected():
            newItem.SetHilight( True )
            
        # As this is a tree we only have to delete the first item. Recursive
        # calls to this method don't need to call this.
        if delete:
            self.Delete( item )
        
        return newItem