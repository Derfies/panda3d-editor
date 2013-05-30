import wx
    

class PreferencesFrame( wx.Frame ):
    
    def __init__( self, *args, **kwargs ):
        kwargs['style'] = wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT
        wx.Frame.__init__( self, *args, **kwargs )
