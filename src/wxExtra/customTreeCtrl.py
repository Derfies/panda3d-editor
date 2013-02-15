import wx
import wx.lib.agw.customtreectrl as ct


class CustomTreeCtrl( ct.CustomTreeCtrl ):
    
    def __init__( self, *args, **kwargs ):
        ct.CustomTreeCtrl.__init__( self, *args, **kwargs )
        
        self.SetBorderPen( wx.Pen( (0, 0, 0), 0, wx.TRANSPARENT ) )
        self.EnableSelectionGradient( True )
        self.SetGradientStyle( True )
        self.SetFirstGradientColour( wx.Color(46, 46, 46) )
        self.SetSecondGradientColour( wx.Color(123, 123, 123) )
    
    def GetItemChildren( self, pItem ):
        """
        wxPython's standard tree control does not have a get item children
        method by default.
        """
        children = []
        
        item, cookie = self.GetFirstChild( pItem )
        while item is not None and item.IsOk():
            children.append( item )
            item = self.GetNextSibling( item )
            
        return children
    
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