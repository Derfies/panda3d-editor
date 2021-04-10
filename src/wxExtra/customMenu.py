import wx

from wxExtra import utils


class CustomMenu( wx.Menu ):
        
    """
    Custom wxMenu class with convenience methods to add menu items with 
    icons.
    """
    
    def AppendActionItem( self, actn, parent ):
        actnText = actn.GetText()
        if not actnText.startswith( '&' ):
            actnText = '&' + actnText
            
        mItem = wx.MenuItem( self, actn.GetId(), actnText )
            
        # Create the icon if iconPath is present
        iconPath = actn.GetIconPath()
        if False:       # Disabled for now
            img = wx.Image( iconPath, wx.BITMAP_TYPE_ANY )
            img.Rescale( 16, 16, quality=wx.IMAGE_QUALITY_HIGH )
            mItem.SetBitmap( img.ConvertToBitmap() )
        
        # Append check item or regular item
        if actn.GetKind() == wx.ITEM_CHECK:
            self.AppendCheckItem( actn.GetId(), actnText )
        else:
            self.Append( mItem )
        
        # Bind the menu event - use args if provided.
        args = actn.GetArguments()
        if args:
            utils.IdBind( parent, wx.EVT_MENU, actn.GetId(), actn.GetCommand(), args )
        else:
            parent.Bind( wx.EVT_MENU, actn.GetCommand(), id=actn.GetId() )
        
    def AppendActionItems( self, actns, parent ):
        for actn in actns:
            self.AppendActionItem( actn, parent )
    
    def AppendIconItem( self, id, text, help, iconPath ):
        
        # Create the icon and resize
        img = wx.Image( iconPath, wx.BITMAP_TYPE_ANY )
        img.Rescale( 16, 16 )
        
        # Create and append the new menu item
        mItem = wx.MenuItem( self, id, text, help )
        mItem.SetBitmap( img.ConvertToBitmap() )
        self.Append( mItem )
        
    def EnableAllTools( self, state ):
        """Enable or disable all tools in the toolbar."""
        for item in self.GetMenuItems():
            item.Enable( state )
            
    def Clear( self ):
        for item in self.GetMenuItems():
            self.DeleteItem( item )