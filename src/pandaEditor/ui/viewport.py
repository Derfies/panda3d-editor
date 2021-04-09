import wx

from p3d.wxPanda import Viewport as WxViewport
from .customDropTarget import CustomDropTarget


class Viewport(WxViewport):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.app = self.GetParent().app
        
        self.dt = CustomDropTarget(['filePath', 'nodePath'], self)
        self.SetDropTarget(self.dt)
        
    def ScreenToViewport( self, x, y ):
        x = ( x / float( self.GetSize()[0] )- 0.5 ) * 2
        y = ( y / float( self.GetSize()[1] ) - 0.5 ) * -2
        return x, y
        
    def GetDroppedObject( self, x, y ):
        x, y = self.ScreenToViewport( x, y )
        return self.app.selection.GetNodePathAtPosition( x, y )