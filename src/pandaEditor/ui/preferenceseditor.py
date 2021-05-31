import wx


class GeneralPage(wx.StockPreferencesPage):

    def CreateWindow(self, parent):
        panel = wx.Panel(parent)
        panel.SetMinSize((600, 300))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, -1, "general page"),
                  wx.SizerFlags(1).TripleBorder())
        panel.SetSizer(sizer)
        return panel
    

class PreferencesEditor(wx.PreferencesEditor):
    
    def __init__(self):
        super().__init__('Preferences')

        class MyPrefsPanel(wx.Panel):
            def __init__(self, parent):
                wx.Panel.__init__(self, parent)
                cb1 = wx.CheckBox(self, -1, "Option 1")
                cb2 = wx.CheckBox(self, -1, "Option 2")
                box = wx.BoxSizer(wx.VERTICAL)
                box.Add(cb1, 0, wx.EXPAND)
                box.Add(cb2, 0, wx.EXPAND)
                self.Sizer = wx.BoxSizer()
                self.Sizer.Add(box, 0, wx.EXPAND)

        class MyPrefsPage(wx.PreferencesPage):
            def GetName(self):
                return 'MyPrefsPage'

            def GetLargeIcon(self):
                return wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR,
                                                (32, 32))

            def CreateWindow(self, parent):
                return MyPrefsPanel(parent)

        page = MyPrefsPage()
        self.AddPage(page)

        page = GeneralPage(0)
        self.AddPage(page)
