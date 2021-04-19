import wx


class ActionItem(object):
    
    def __init__(self, text, iconPath, cmd, id=None, args=[], helpStr='', 
                  kind=wx.ITEM_NORMAL):
        self._text = text
        self._iconPath = iconPath
        self._cmd = cmd
        self._id = id
        self._args = args
        self._helpStr = helpStr
        self._kind = kind
        
        # Generate a unique id if one wasn't supplied
        if self._id is None:
            self._id = wx.NewId()
            
    def GetText(self):
        return self._text
    
    def GetIconPath(self):
        return self._iconPath
    
    def GetCommand(self):
        return self._cmd
            
    def GetId(self):
        return self._id
    
    def GetArguments(self):
        return self._args
    
    def GetHelpString(self):
        return self._helpStr
    
    def GetKind(self):
        return self._kind
