import wx
    

class ProjectSettingsPanel(wx.Panel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Project directory
        bs1 = wx.BoxSizer(wx.HORIZONTAL)
        bs1.Add(wx.StaticText(self, -1, 'Project Directory:'), 1, wx.RIGHT, 10)
        bs1.Add(wx.TextCtrl(self, -1, '', size=(125, -1)), 1, wx.RIGHT, 10)
        bs1.Add(wx.Button(self, -1), 1)
        
        # Project name
        bs2 = wx.BoxSizer(wx.HORIZONTAL)
        bs2.Add(wx.StaticText(self, -1, 'Project Name:'), 1, wx.RIGHT, 10)
        bs2.Add(wx.TextCtrl(self, -1, '', size=(125, -1)), 1, wx.RIGHT, 10)
        bs2.Add(wx.Button(self, -1, '...'), 1)
        
        # Build sizers
        bs = wx.BoxSizer(wx.VERTICAL)
        bs.Add(bs1, 0)
        bs.Add(bs2, 0)
        
        # Build border
        self.border = wx.BoxSizer(wx.VERTICAL)
        self.border.Add(bs, 1, wx.ALL, 10)
        self.SetSizer(self.border)
