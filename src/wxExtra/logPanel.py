import sys

import wx


class LogPanel(wx.Panel):
    
    """
    Simple wxPanel containing a text control which will display the stdout and
    stderr streams.
    """
    
    class RedirectText(object):
        
        def __init__(self, terminal, textCtrl):
            self.terminal = terminal
            self.textCtrl = textCtrl
            
            # Set err to True if the stream is stderr
            self.err = False
            if terminal is sys.stderr:
                self.err = True

        def write(self, text):
            self.terminal.write(text)
            self.textCtrl.WriteText(text)
            
            # If the text came from stderr, thaw the top window of the 
            # application or else we won't see the message!
            if self.err:
                wx.CallAfter(self.ThawTopWindow)
                
        def ThawTopWindow(self):
            """
            If the application has thrown an assertion while the top frame has
            been frozen then we won't be able to see the text. This method once
            called after the write() method above will make sure the top frame
            is thawed - making the text visible.
            """
            topWin = wx.GetApp().GetTopWindow()
            if topWin.IsFrozen():
                topWin.Thaw()
    
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        
        # Build log text control
        self.tc = wx.TextCtrl(self, style=
                               wx.TE_MULTILINE | 
                               wx.TE_RICH2 |
                               wx.NO_BORDER)
        
        # Redirect text here
        sys.stdout = self.RedirectText(sys.stdout, self.tc)
        sys.stderr = self.RedirectText(sys.stderr, self.tc)
        
        # Build sizers
        self.bs1 = wx.BoxSizer(wx.VERTICAL)
        self.bs1.Add(self.tc, 1, wx.EXPAND)
        self.SetSizer(self.bs1)