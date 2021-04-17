import wx

import wxExtra
from wxExtra import utils


class CustomAuiToolBar(wx.aui.AuiToolBar):
    
    def __init__(self, *args, **kwargs):
        wx.aui.AuiToolBar.__init__(self, *args, **kwargs)
        self._bmpSize = None
    
    def AppendActionItem(self, actn):
        wx.Log.SetLogLevel(0) # Icon gives an sRGB error but still displays. This suppresses the error.
        actnIcon = wxExtra.utils.ImgToBmp(actn.GetIconPath(), self.GetToolBitmapSize())
        self.AddTool(actn.GetId(), actn.GetText(), actnIcon,
                     actn.GetHelpString(), actn.GetKind())
        self.Bind(wx.EVT_TOOL, actn.GetCommand(), id=actn.GetId())
        
    def AppendActionItems(self, actns):
        for actn in actns:
            self.AppendActionItem(actn)
        
    def GetToolBitmapSize(self):
        """
        Workaround as GetToolBitmapSize seems only to return the default
        icon size.
        """
        if self._bmpSize is None:
            return wx.aui.AuiToolBar.GetToolBitmapSize(self)
        
        return self._bmpSize
        
    def SetToolBitmapSize(self, size):
        """
        Workaround as GetToolBitmapSize seems only to return the default
        icon size.
        """
        wx.aui.AuiToolBar.SetToolBitmapSize(self, size)
        
        self._bmpSize = size
        
    def EnableAllTools(self, state):
        """Enable or disable all tools in the toolbar."""
        for i in range(self.GetToolCount()):
            tool = self.FindToolByIndex(i)
            self.EnableTool(tool.GetId(), state)
        self.Refresh()
    