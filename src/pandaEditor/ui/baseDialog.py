import wx


class BaseDialog(wx.Dialog):

    def __init__(self, Panel, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Build the panel
        self.pnl = Panel(self)
        
        # Build sizers
        bs1 = wx.BoxSizer(wx.VERTICAL)
        bs1.Add(self.pnl, 1, wx.EXPAND, 0)
        self.SetSizer(bs1)
        
        # Resize list control to fit
        #self.SetSize((self.GetSize().x, self.pnl.GetBestSizeY())) 
        self.Fit()
        
        # Layout
        self.CenterOnScreen()
