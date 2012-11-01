import wx
import wx.lib.agw.customtreectrl as ct

from sceneGraphBasePanel import SceneGraphBasePanel


class LightLinkerPanel( wx.Panel ):
    
    def __init__( self, *args, **kwargs ):
        wx.Panel.__init__( self, *args, **kwargs )
       
        # Build splitter and panels
        self.splt = wx.SplitterWindow( self )
        pnlLeft = SceneGraphBasePanel( self.splt )
        pnlRight = SceneGraphBasePanel( self.splt )

        # Split the window
        self.splt.SplitVertically( pnlLeft, pnlRight )
        self.splt.SetMinimumPaneSize( 20 )

        sizer = wx.BoxSizer( wx.VERTICAL )
        sizer.Add( self.splt, 1, wx.EXPAND )
        self.SetSizer( sizer )