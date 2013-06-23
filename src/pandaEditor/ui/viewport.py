import wx

import p3d
from customDropTarget import CustomDropTarget


class Viewport( p3d.wx.Viewport ):
    
    def __init__( self, *args, **kwargs ):
        p3d.wx.Viewport.__init__( self, *args, **kwargs )
        
        self.app = wx.GetApp()
        
        self.dt = CustomDropTarget( ['filePath', 'nodePath'], self )
        self.SetDropTarget( self.dt )
        
    def ScreenToViewport( self, x, y ):
        x = ( x / float( self.GetSize()[0] )- 0.5 ) * 2
        y = ( y / float( self.GetSize()[1] ) - 0.5 ) * -2
        return x, y
        
    def GetDroppedObject( self, x, y ):
        x, y = self.ScreenToViewport( x, y )
        return self.app.selection.GetNodePathAtPosition( x, y )