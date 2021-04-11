import os
import sys
import tempfile
import traceback

import wx

import p3d
from .. import gamePlugin as gp
from ..gamePlugin.pandaObject import PandaObjectNPO
from ..gamePlugin.constants import *
from pandaEditor import commands as cmds, actions
from wxExtra import utils as wxUtils, ActionItem, CustomAuiToolBar


TBAR_ICON_SIZE = (24, 24)
TEMP_SCENE_PATH = os.path.join(tempfile.gettempdir(), 'temp.xml')

ID_WIND_PLAY_TOOLBAR = wx.NewId()

ID_PLAY = wx.NewId()
ID_PAUSE = wx.NewId()
    

class EditorPlugin(gp.GamePlugin):
        
    def OnInit(self):
        gp.GamePlugin.OnInit(self)
        
        self.playing = False
        
        # Add new commands to command module.
        setattr(cmds, 'AddScript', self.AddScript)
        
        self.AddDragDropFileTypeHandler('.py', self.DropScript)
        self.AddDragDropFileTypeHandler('.pyc', self.DropScript)
        
        self.app.accept('escape', self.OnPause)
        
        self.BuildPlaybackToolBar()
        
        panelInfo = (wx.aui.AuiPaneInfo()
                      .Name('tbPlay')
                      .Caption('Playback Toolbar')
                      .ToolbarPane()
                      .Top())
        self.AddUiWindow(ID_WIND_PLAY_TOOLBAR, self.tbPlay, panelInfo)
        
    def BuildPlaybackToolBar(self):
        """Build playback toolbar."""
        dirPath = os.path.join(os.path.split(__file__)[0], 'images')
        playbackActns = [
            ActionItem('Play', os.path.join(dirPath, 'play.png'), self.OnPlay, ID_PLAY, 'Play'),
            ActionItem('Pause', os.path.join(dirPath, 'pause.png'), self.OnPause, ID_PAUSE, 'Pause')
        ]
        self.tbPlay = CustomAuiToolBar(self.ui, -1)
        self.tbPlay.SetToolBitmapSize(TBAR_ICON_SIZE)
        self.tbPlay.AppendActionItems(playbackActns)
        
    def AddScript(self, np, filePath):
        
        # Try to load the script. Warn the user if the script fails in any 
        # way.
        try:
            scriptWrprCls = base.game.nodeMgr.nodeWrappers['Script']
            scriptWrpr = scriptWrprCls.Create(filePath=filePath)
        except:
            wxUtils.ErrorDialog(traceback.format_exc(), 'Script Error')
            return
        
        # A NodePath needs a PandaObject as an anchor in order to attach a
        # script to it. Create one if it doesn't already exist and add it to
        # the list of undoable actions.
        actns = []
        pObjWrprCls = base.game.nodeMgr.nodeWrappers[TAG_PANDA_OBJECT]
        pObj = PandaObjectNPO.Get(np)
        if pObj is None:
            pObjWrpr = pObjWrprCls.Create()
            actns.append(actions.Add(pObjWrpr.data))
        else:
            pObjWrpr = pObjWrprCls(pObj)
        pObjWrpr.SetParent(np)
        scriptWrpr.SetParent(pObjWrpr.data)
        actns.append(actions.Add(scriptWrpr.data))
        
        # Create a composite action, exectute it and push it onto the undo
        # queue.
        actn = actions.Composite(actns)
        wx.GetApp().actnMgr.Push(actn)
        actn()
        wx.GetApp().doc.OnModified()
        
    def DropScript(self, filePath, np=None):
        """Drag drop handler for attaching scripts to NodePaths."""
        if np is not None:
            cmds.AddScript(np, filePath)
        
    def OnPlay(self, evt=None):
        
        # Set playing flag
        if self.playing:
            return
        self.playing = True
        
        # Save temp scene file
        self.app.scene.Save(filePath=TEMP_SCENE_PATH)
        
        # Start panda behaviours
        base.pandaMgr.Init()
        base.pandaMgr.Start()
        
        # Update UI
        self.app.doc.OnRefresh()
        
    def OnPause(self, evt=None):
        
        # Set playing flag
        if not self.playing:
            return
        self.playing = False
        
        # Stop panda behaviours
        base.pandaMgr.Stop()
        base.pandaMgr.Del()
        
        # Set up a new scene and load the contents of the temp scene saved
        # before the user pressed play
        oldPath = self.app.doc.filePath
        self.app.CreateScene(TEMP_SCENE_PATH, newDoc=False)
        self.app.scene.Load(filePath=TEMP_SCENE_PATH)
        self.app.doc.filePath = oldPath
        
        # Set the document contents back to the temp scene we loaded
        self.app.doc.contents = self.app.scene
        self.app.doc.OnRefresh()
        
    def OnUpdate(self, msg):
        
        # Disable all toolbar tools
        self.tbPlay.EnableAllTools(False)
        
        # Enable the pause tool if in play mode
        if self.playing:
            self.tbPlay.EnableTool(ID_PAUSE, True)
        else:
            self.tbPlay.EnableTool(ID_PLAY, True)
        
        # Refresh toolbars in order to show changes
        self.tbPlay.Refresh()
        
    def OnProjectFilesModified(self, filePaths):
        
        # Don't reload files during playback. They will be reloaded once
        # playback is finished anyway when the scene is reloaded.
        if self.playing:
            return
        
        # Get .py files
        pyFilePaths = []
        for filePath in filePaths:
            if os.path.splitext(filePath)[1] == '.py':
                pyFilePaths.append(filePath)
        
        # Reload scripts
        if pyFilePaths:
            
            for pyFilePath in pyFilePaths:
                print 'Reloading script: ', pyFilePath
            
            nps = [
                np 
                for np in base.scene.rootNp.findAllMatches('**/*')
                if np.getPythonTag(TAG_PANDA_OBJECT) is not None
            ]
            for np in nps:
                pObjWrpr = base.game.nodeMgr.Wrap(PandaObjectNPO.Get(np))
                for pyFilePath in pyFilePaths:
                    pObjWrpr.ReloadScript(pyFilePath)