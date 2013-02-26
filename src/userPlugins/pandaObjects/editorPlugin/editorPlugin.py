import os
import sys
import tempfile
import traceback

import wx

import p3d
from .. import gamePlugin as gp
from wxExtra import utils as wxUtils, ActionItem, CustomAuiToolBar


TBAR_ICON_SIZE = (24, 24)
TEMP_SCENE_PATH = os.path.join( tempfile.gettempdir(), 'temp.xml' )

ID_WIND_PLAY_TOOLBAR = wx.NewId()

ID_PLAY = wx.NewId()
ID_PAUSE = wx.NewId()
    

class EditorPlugin( gp.GamePlugin ):
        
    def OnInit( self ):
        gp.GamePlugin.OnInit( self )
        
        self.playing = False
        
        self.app.fileTypes['.py'] = self.AddScript
        self.app.fileTypes['.pyc'] = self.AddScript
        
        self.app.accept( 'escape', self.OnPause )
        
        self.BuildPlaybackToolBar()
        
        paneDefs = {    
            ID_WIND_PLAY_TOOLBAR:(self.tbPlay, True,
                wx.aui.AuiPaneInfo()
                .Name( 'tbPlay' )
                .Caption( 'Playback Toolbar' )
                .ToolbarPane()
                .Top())
        }
                
        for paneDef in paneDefs.values():
            self.ui._mgr.AddPane( paneDef[0], paneDef[2] )
            
        self.ui._mgr.Update()
        
        # DEBUG
        base.pandaMgr = p3d.PandaManager()
        
    def BuildPlaybackToolBar( self ):
        """Build playback toolbar."""
        dirPath = os.path.join( os.path.split( __file__ )[0], 'images' )
        playbackActns = [
            ActionItem( 'Play', os.path.join( dirPath, 'play.png' ), self.OnPlay, ID_PLAY, 'Play' ),
            ActionItem( 'Pause', os.path.join( dirPath, 'pause.png' ), self.OnPause, ID_PAUSE, 'Pause' )
        ]
        self.tbPlay = CustomAuiToolBar( self.ui, -1, style=wx.aui.AUI_TB_DEFAULT_STYLE )
        self.tbPlay.SetToolBitmapSize( TBAR_ICON_SIZE )
        self.tbPlay.AppendActionItems( playbackActns )
        
    def AddScript( self, filePath, np=None ):
        
        # Bail if no node path was supplied.
        if np is None:
            return
        
        pObjWrpr = gp.PandaObject()#
        pObjWrpr.Create()
        pObjWrpr.SetParent( np )
        
        scriptWrpr = gp.Script()
        scriptWrpr.Create( filePath=filePath )
        scriptWrpr.SetParent( pObjWrpr.data )
        
        self.app.doc.OnModified()
        
        # Attempt to attach the script. Warn the user if the script fails in 
        # any way.
        #try:
        #if True:
        #    pObj = gp.PandaObject().Create( np )
        #    pObj.AttachScript( filePath )
        #except:
        #    wxUtils.ErrorDialog( traceback.format_exc(), 'Script Error' )
        #    return
        
        #self.app.doc.OnModified()
        
    def OnPlay( self, evt=None ):
        
        # Set playing flag
        if self.playing:
            return
        self.playing = True
        
        # Save temp scene file
        self.app.scene.Save( filePath=TEMP_SCENE_PATH )
        
        # Start panda behaviours
        base.pandaMgr.Init()
        base.pandaMgr.Start()
        
        # Update UI
        self.app.doc.OnRefresh()
        
    def OnPause( self, evt=None ):
        
        # Set playing flag
        if not self.playing:
            return
        self.playing = False
        
        # Stop panda behaviours
        base.pandaMgr.Stop()
        base.pandaMgr.Del()
        
        # Set up a new scene and load the contents of the temp scene saved
        # before the user pressed play
        oldPath = self.app.scene.filePath
        self.app.CreateScene( TEMP_SCENE_PATH, newDoc=False )
        self.app.scene.Load( filePath=TEMP_SCENE_PATH )
        self.app.scene.filePath = oldPath
        
        # Set the document contents back to the temp scene we loaded
        self.app.doc.contents = self.app.scene
        self.app.doc.OnRefresh()
        
    def OnUpdate( self, msg ):
        
        # Disable all toolbar tools
        #self.ui.tbFile.EnableAllTools( False )
        self.tbPlay.EnableAllTools( False )
        
        # Enable the pause tool if in play mode
        if self.playing:
            self.tbPlay.EnableTool( ID_PAUSE, True )
        else:
            #self.ui.tbFile.EnableAllTools( True )
            self.tbPlay.EnableTool( ID_PLAY, True )
        
        # Refresh toolbars in order to show changes
        self.tbPlay.Refresh()
        
    def OnProjectFilesModified( self, filePaths ):
        
        # Don't reload files during playback. They will be reloaded once
        # playback is finished anyway when the scene is reloaded.
        if self.playing:
            return
        
        # Get .py files
        pyFilePaths = []
        for filePath in filePaths:
            if os.path.splitext( filePath )[1] == '.py':
                pyFilePaths.append( filePath )
        
        # Reload scripts
        if pyFilePaths:
            base.pandaMgr.ReloadScripts( pyFilePaths )
        
    def GetScriptRelPath( self, filePath ):
        """
        Attempt to find the indicated file path on one of the paths in 
        sys.path. If found then return a path relative to it.
        """
        # TO DO: Still a bit funky how we do this as it could grab whatever
        # sys.path that matches first, which won't necessarily be the one we
        # want. Perhaps fix with extra config vars like getModelPath()?
        filePath = os.path.normpath( filePath )
        for sysPath in sys.path:
            if sysPath in filePath:
                filePath = os.path.relpath( filePath, sysPath )
                break
                        
        return filePath