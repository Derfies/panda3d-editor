import wx
import wx.lib.mixins.listctrl as listmix


class CustomListCtrl( wx.ListCtrl, listmix.ListCtrlAutoWidthMixin ):
    
    def __init__( self, *args, **kwargs ):
        wx.ListCtrl.__init__( self, *args, **kwargs )
        listmix.ListCtrlAutoWidthMixin.__init__( self )
    
    def GetSelections( self ):
        """
        Gets the selected items for the list control.
        Selection is returned as a list of selected indices, low to high.
        """
        selections = []

        # Start at -1 to get the first selected item
        current = -1
        while True:
            next = self.GetNextSelected( current )
            if next == -1:
                return selections
            
            selections.append( next )
            current = next
            
        return selections
    
    def GetAllItems( self ):
        """Return a list of all items in the control."""
        items = []
        for i in range( self.GetItemCount() ):
            items.append( self.GetItem( i ) )
                         
        return items
    
    def FindItems( self, start, strs, partial ):
        """Return a list with all find results for each input string."""
        items = []
        for str in strs:
            items.append( self.FindItem( start, str, partial ) )
                         
        return items
    
    def FindItemByData( self, data ):
        """
        Return the index for the item in the list which owns the supplied 
        data.
        """
        for i in range( self.GetItemCount() ):
            if self.GetItem( i ).GetPyData() == data:
                return i
            
        # No match found, return -1
        return -1