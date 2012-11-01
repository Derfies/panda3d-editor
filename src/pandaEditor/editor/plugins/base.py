import wx
from oldGame.plugins.base import Base as OldBase


class Base( OldBase ):
    
    def __init__( self, *args, **kwargs ):
        OldBase.__init__( self, *args, **kwargs )
        
        self.app = wx.GetApp()
        self.ui = self.app.frame
        
    def OnInit( self, *args, **kwargs ):
        OldBase.OnInit( self, *args, **kwargs )
        
    def OnUpdate( self, msg ):
        pass
        
    def OnSceneClose( self ):
        pass
    
    def OnProjectFilesModified( self, filePaths ):
        pass