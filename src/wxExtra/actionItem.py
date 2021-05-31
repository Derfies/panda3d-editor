import wx


class ActionItem:
    
    def __init__(self, text, iconPath, cmd, id=None, args=None, kwargs=None,
                 helpStr='', kind=wx.ITEM_NORMAL):
        self._text = text
        self._iconPath = iconPath
        self._cmd = cmd
        self._id = id
        self._args = args or []
        self._kwargs = kwargs or {}
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

    def GetKwarguments(self):
        return self._kwargs
    
    def GetHelpString(self):
        return self._helpStr
    
    def GetKind(self):
        return self._kind
