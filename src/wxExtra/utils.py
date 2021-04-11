import os

import wx


def FileDialog(message, wildcard, style, defaultDir=os.getcwd(), defaultFile=''):
    """
    Generic file dialog method. If False is returned then the user has hit
    cancel or not selected a valid path.
    """
    result = []
    dlg = wx.FileDialog(wx.GetApp().GetTopWindow(), message, defaultDir, defaultFile, wildcard, style)
    if dlg.ShowModal() == wx.ID_OK:
        if style & wx.FD_MULTIPLE:
            result = dlg.GetPaths()
        else:
            result = [dlg.GetPath()]
    dlg.Destroy()
    return result
    

def FileOpenDialog(message, wildcard, style=0, defaultDir=os.getcwd(), defaultFile=''):
    """Generic file open dialog."""
    style = style | wx.FD_OPEN | wx.FD_CHANGE_DIR
    return FileDialog(message, wildcard, style, defaultDir, defaultFile)
    

def FileSaveDialog(message, wildcard, style=0, defaultDir=os.getcwd(), defaultFile=''):
    """Generic file save dialog."""
    style = style | wx.FD_SAVE | wx.FD_CHANGE_DIR
    file_paths = FileDialog(message, wildcard, style, defaultDir, defaultFile)
    return next(iter(file_paths), None)
    

def DirDialog(message, defaultPath=os.getcwd(), style=wx.DD_DEFAULT_STYLE):
    """Generic directory dialog."""
    dlg = wx.DirDialog(wx.GetApp().GetTopWindow(), message, defaultPath, style)
    if dlg.ShowModal() == wx.ID_OK:
        result = dlg.GetPath()
    else:
        result = False
    dlg.Destroy()
    
    return result
    

def MessageDialog(message, caption, style):
    """Generic message dialog method."""
    dlg = wx.MessageDialog(wx.GetApp().GetTopWindow(), message, caption, style)
    result = dlg.ShowModal()
    dlg.Destroy()
    
    return result
    

def InformationDialog(message, caption='Information'):
    """Generic information dialog with ok button."""
    return MessageDialog(message, caption, wx.ICON_INFORMATION | wx.OK)
    

def WarningDialog(message, caption='Warning'):
    """Generic warning dialog with ok button."""
    return MessageDialog(message, caption, wx.ICON_WARNING | wx.OK)
    

def ErrorDialog(message, caption='Error'):
    """Generic error dialog with ok button."""
    return MessageDialog(message, caption, wx.ICON_ERROR | wx.OK)
    

def YesNoDialog(message, caption, style=wx.ICON_QUESTION):
    """Generic message dialog with yes / no buttons."""
    return MessageDialog(message, caption, style | wx.YES_NO)
    

def YesNoCancelDialog(message, caption, style=wx.ICON_QUESTION):
    """Generic message dialog with yes / no / cancel buttons."""
    return MessageDialog(message, caption, style | wx.YES_NO | wx.CANCEL)
    

def ImgToBmp(filePath, size):
    """Return a wx bitmap from a filepath, scaled to the toolbar size."""
    img = wx.Image(filePath)
    img.Rescale(size[0], size[1])
    bmp = wx.Bitmap(img)
    return bmp
    

def BetterBind(self, event, instance, handler, *args, **kwargs):
    self.Bind(event, lambda event: handler(event, *args, **kwargs), instance)
    
    
def IdBind(self, event, id, handler, *args, **kwargs):
    self.Bind(event, lambda event: handler(event, *args, **kwargs), id=id)
    

def GetClickedItem(ctrl, evt):
    """Return the id for the item involved in the mouse event."""
    return ctrl.HitTest(wx.Point(evt.GetX(), evt.GetY()))[0]
