import sys

import wx
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import WindowProperties


keyCodes = {
    wx.WXK_SPACE: 'space',
    wx.WXK_DELETE: 'del',
    wx.WXK_ESCAPE: 'escape',
    wx.WXK_BACK: 'backspace',
    wx.WXK_CONTROL: 'control',
    wx.WXK_ALT: 'alt',
    wx.WXK_UP: 'arrow_up',
    wx.WXK_DOWN: 'arrow_down',
    wx.WXK_LEFT: 'arrow_left',
    wx.WXK_RIGHT: 'arrow_right'
}


def OnKey( evt, action='' ):
    """
    Bind this method to a wx.EVT_KEY_XXX event coming from a wx panel or other
    widget, and it will stop wx 'eating' the event and passing it to Panda's 
    base class instead.
    """
    keyCode = evt.GetKeyCode()
    if keyCode in keyCodes:
        messenger.send( keyCodes[keyCode] + action )
    elif keyCode in range( 256 ):
        
        # Test for any other modifiers. Add these in the order shift, control,
        # alt
        mod = ''
        if evt.ShiftDown():
            mod += 'shift-'
        if evt.ControlDown():
            mod += 'control-'
        if evt.AltDown():
            mod += 'alt-'
        char = chr( keyCode ).lower()
        messenger.send( mod + char + action )
        

def OnKeyUp( evt ):
    OnKey( evt, '-up' )
    

def OnKeyDown( evt ):
    OnKey( evt )
    

def OnLeftUp( evt ):
    messenger.send( 'mouse1-up' )
    

class Viewport( wx.Panel ):
    
    def __init__( self, *args, **kwargs ):
        """
        Initialise the wx panel. You must complete the other part of the
        init process by calling Initialize() once the wx-window has been
        built.
        """
        wx.Panel.__init__( self, *args, **kwargs )
        
        self._win = None
        
    # def GetWindow( self ):
    #     return self._win
    #
    # def SetWindow( self, win ):
    #     self._win = win
        
    def Initialize( self, useMainWin=True ):
        """
        The panda3d window must be put into the wx-window after it has been
        shown, or it will not size correctly.
        """
        assert self.GetHandle() != 0
        wp = WindowProperties()
        wp.setOrigin( 0, 0 )
        wp.setSize( self.ClientSize.GetWidth(), self.ClientSize.GetHeight() )
        wp.setParentWindow( self.GetHandle() )
        if self._win is None:
            if useMainWin:
                base.openDefaultWindow( props=wp, gsg=None )
                self._win = base.win
            else:
                self._win = base.openWindow( props=wp, makeCamera=0 )
        self.Bind( wx.EVT_SIZE, self.OnResize )
        
    def OnResize( self, event ):
        """When the wx-panel is resized, fit the panda3d window into it."""
        frame_size = event.GetSize()
        wp = WindowProperties()
        wp.setOrigin( 0, 0 )
        wp.setSize( frame_size.GetWidth(), frame_size.GetHeight() )
        self._win.requestProperties( wp )
        

class App( wx.App, DirectObject ):
    
    """
    Don't forget to bind your frame's wx.EVT_CLOSE event to the app's
    self.Quit method, or the application will not close properly.
    """
        
    def ReplaceEventLoop( self ):
        self.evtLoop = wx.EventLoop()
        self.oldLoop = wx.EventLoop.GetActive()
        wx.EventLoop.SetActive( self.evtLoop )
        taskMgr.add( self.WxStep, 'evtLoopTask' )
        self.WxStep()
        
    def OnDestroy( self, event=None ):
        self.WxStep()
        wx.EventLoop.SetActive( self.oldLoop )
        
    def Quit( self, event=None ):
        self.OnDestroy( event )
        try:
            base
        except NameError:
            sys.exit()
        base.userExit()
        
    def WxStep( self, task=None ):
        while self.evtLoop.Pending():
            self.evtLoop.Dispatch()
        self.ProcessIdle()
        if task != None:
            return task.cont