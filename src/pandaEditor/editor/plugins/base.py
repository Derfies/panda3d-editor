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
    
    def AddUiWindow( self, id, ctrl, auiInfo, showInWindowMenu=True ):
        self.app.frame.paneDefs[id] = (ctrl, showInWindowMenu, auiInfo)
        self.app.frame.RebuildPanelMenu()
        self.ui._mgr.AddPane( ctrl, auiInfo )
        self.ui._mgr.Update()
        
    def AddDragDropFileTypeHandler( self, ext, fn ):
        if ext not in self.app.dDropMgr.fileTypes:
            self.app.dDropMgr.fileTypes[ext] = fn
        else:
            raise Warning( ext + ' already has a file type handler' )
        