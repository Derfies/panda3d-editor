import os

import wx

import p3d
from wxExtra import CompositeDropTarget


class Viewport( p3d.wx.Viewport ):
    
    def __init__( self, *args, **kwargs ):
        p3d.wx.Viewport.__init__( self, *args, **kwargs )
        
        self.dt = CompositeDropTarget( ['filePath'], self.OnDropItem, self.ValidateDropItem )
        self.SetDropTarget( self.dt )
    
    def OnDropItem( self, arg ):
        
        # Do the actual dropping next frame. This will allow the picker time
        # to traverse the scene and find the node the mouse is over.
        taskMgr.doMethodLater( 0, wx.GetApp().OnDragDrop, 'dragDrop', [arg] )
        
    def ValidateDropItem( self, x, y ):
        return True
    