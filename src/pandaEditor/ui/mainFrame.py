import os
import sys

import wx
import wx.aui
from wx.lib.pubsub import Publisher as pub
import pandac.PandaModules as pm
from direct.actor.Actor import Actor

import p3d
from .. import commands as cmds
from wxExtra import utils as wxUtils, ActionItem, LogPanel, CustomMenu
from wxExtra import AuiManagerConfig, CustomAuiToolBar, CustomMenu
from viewport import Viewport
from pandaEditor import game
from document import Document
from baseDialog import BaseDialog
from resourcesPanel import ResourcesPanel
from propertiesPanel import PropertiesPanel
from sceneGraphPanel import SceneGraphPanel
from lightLinkerPanel import LightLinkerPanel
from projectSettingsPanel import ProjectSettingsPanel


FRAME_TITLE = 'Panda Editor 0.1'
TBAR_ICON_SIZE = (24, 24)
WILDCARD_MODEL = 'Model (*.egg; *.bam; *.egg.pz)|*.egg;*.bam;*.egg.pz'
WILDCARD_SCENE = '.xml|*.xml'
WILDCARD_P3D = '.p3d|*.p3d'

ID_FILE_NEW = wx.NewId()
ID_FILE_OPEN = wx.NewId()
ID_FILE_SAVE = wx.NewId()
ID_FILE_SAVE_AS = wx.NewId()
ID_FILE_IMPORT = wx.NewId()
ID_FILE_PROJ = wx.NewId()

ID_PROJ_NEW = wx.NewId()
ID_PROJ_SET = wx.NewId()
ID_PROJ_BUILD = wx.NewId()

ID_EDIT_UNDO = wx.NewId()
ID_EDIT_REDO = wx.NewId()
ID_EDIT_GROUP = wx.NewId()
ID_EDIT_UNGROUP = wx.NewId()
ID_EDIT_PARENT = wx.NewId()
ID_EDIT_UNPARENT = wx.NewId()

ID_MODIFY_PHYSICS = wx.NewId()

ID_XFORM_SEL = wx.NewId()
ID_XFORM_POS = wx.NewId()
ID_XFORM_ROT = wx.NewId()
ID_XFORM_SCL = wx.NewId()
ID_XFORM_WORLD = wx.NewId()

ID_VIEW_GRID = wx.NewId()
ID_VIEW_TOP = wx.NewId() 
ID_VIEW_BOTTOM = wx.NewId() 
ID_VIEW_FRONT = wx.NewId() 
ID_VIEW_BACK = wx.NewId() 
ID_VIEW_RIGHT = wx.NewId() 
ID_VIEW_LEFT = wx.NewId() 

ID_LAYOUT_GAME = wx.NewId() 
ID_LAYOUT_EDITOR = wx.NewId() 
ID_LAYOUT_BOTH = wx.NewId() 

ID_WIND_FILE_TOOLBAR = wx.NewId()
ID_WIND_EDIT_TOOLBAR = wx.NewId()
ID_WIND_MODIFY_TOOLBAR = wx.NewId()
ID_WIND_XFORM_TOOLBAR = wx.NewId()
ID_WIND_LAYOUT_TOOLBAR = wx.NewId()
ID_WIND_VIEWPORT = wx.NewId()
ID_WIND_SCENE_GRAPH = wx.NewId()
ID_WIND_LIGHT_LINKER = wx.NewId()
ID_WIND_PROPERTIES = wx.NewId()
ID_WIND_RESOURCES = wx.NewId()
ID_WIND_LOG = wx.NewId()

ID_PLAY = wx.NewId()
ID_PAUSE = wx.NewId()


class MainFrame( wx.Frame ):
    
    """Panda Editor user interface."""

    def __init__( self, *args, **kwargs ):
        wx.Frame.__init__( self, *args, **kwargs )
        
        self.app = wx.GetApp()
        self.preMaxPos = None
        self.preMaxSize = None
        self.actns = {
            ID_EDIT_UNDO:self.app.Undo,
            ID_EDIT_REDO:self.app.Redo,
            ID_EDIT_GROUP:self.app.Group,
            ID_EDIT_UNGROUP:self.app.Ungroup,
            ID_EDIT_PARENT:self.app.Parent,
            ID_EDIT_UNPARENT:self.app.Unparent
        }
        
        # Bind frame events
        self.Bind( wx.EVT_CLOSE, self.OnClose )
        self.Bind( wx.EVT_KEY_UP, p3d.wx.OnKeyUp )
        self.Bind( wx.EVT_KEY_DOWN, p3d.wx.OnKeyDown )
        self.Bind( wx.EVT_SIZE, self.OnSize )
        self.Bind( wx.EVT_MOVE, self.OnMove )
        
        # Bind publisher events
        pub.subscribe( self.OnUpdate, 'Update' )
        
        # Build application preferences
        self.cfg = wx.Config( 'pandaEditor' )
        
        # Build toolbars
        self.BuildFileActions()
        self.BuildEditActions()
        self.BuildModifyActions()
        self.BuildXformActions()
        self.BuildLayoutActions()
        
        # Build viewport. Don't initialise just yet as ShowBase has not yet 
        # been created.
        self.pnlViewport = Viewport( self )
        
        # Build editor panels
        self.pnlSceneGraph = SceneGraphPanel( self, style=wx.SUNKEN_BORDER )
        self.pnlLightLinker = LightLinkerPanel( self, style=wx.SUNKEN_BORDER )
        self.pnlProps = PropertiesPanel( self, style=wx.SUNKEN_BORDER )
        self.pnlRsrcs = ResourcesPanel( self, style=wx.SUNKEN_BORDER )
        self.pnlLog = LogPanel( self, style=wx.SUNKEN_BORDER )
        
        # Build aui manager to hold all the widgets
        self.BuildAuiManager()
        
        # Build menus and menu bar
        self.mb = wx.MenuBar()
        self.BuildViewMenu()
        self.BuildCreateMenu()
        self.BuildWindowMenu()
        self.BuildMenuBar()
        
        # Update the view menu based on the perspective saved in preferences
        self.OnUpdateWindowMenu( None )
        
    def _GetSavePath( self ):
                
        # Get default paths from current project directory, or the scene's
        # current location on disk
        defaultDir = ''
        defaultFile = ''
        if self.app.doc.contents.filePath is not None:
            defaultDir, defaultFile = os.path.split( self.app.doc.contents.filePath )
        elif self.app.project.path is not None:
            defaultDir = self.app.project.GetScenesDirectory()

        # Open file browser
        filePath = wxUtils.FileSaveDialog( 'Save Scene As', WILDCARD_SCENE, defaultDir=defaultDir, defaultFile=defaultFile )
        if filePath and os.path.exists( filePath ):

            # Warn user if the chosen file path already exists
            msg = ''.join( ['The file "', filePath, '" already exists.\nDo you want to replace it?'] )
            if wxUtils.YesNoDialog( msg, 'Replace File?', wx.ICON_WARNING ) == wx.ID_NO:
                return False

        return filePath
    
    def _CheckForSave( self ):
        """
        If there is already a file loaded and it is dirty, query the user to
        save the file. Return False for cancel, True otherwise.
        """
        if self.app.doc.dirty:

            # Show dialog, record result
            msg = ''.join( ['The document "', self.app.doc.title, '" was modified after last save.\nSave changes before continuing?'] )
            result = wxUtils.YesNoCancelDialog( msg, 'Save Changes?', wx.ICON_WARNING )
            if result == wx.ID_YES:
                self.OnFileSave( None )
            elif result == wx.ID_CANCEL:
                return False

        # Document not dirty, return True
        return True
        
    def OnClose( self, evt ):
        """Save frame and aui preferences, hide the window and quit."""
        # Check if ok to continue, stop the closing process if the user
        # cancelled
        if not self._CheckForSave():
            evt.Veto()
            return
        
        # Save prefs, hide window and quit
        self.auiCfg.Save()
        if self.preMaxPos is not None:
            self.auiCfg.SavePosition( *self.preMaxPos )
        if self.preMaxSize is not None:
            self.auiCfg.SaveSize( *self.preMaxSize )
        if self.app.project.path is not None:
            self.cfg.Write( 'projDirPath', self.app.project.path )
        self.Show( False )
        self.app.Quit()
        
    def OnFileNew( self, evt ):
        """Show project settings panel and create new scene."""
        # Check if ok to continue, return if the user cancelled
        if not self._CheckForSave():
            return
        
        # Create new document
        self.app.CreateScene()
        self.app.doc.OnRefresh()
        
    def OnFileOpen( self, evt, filePath=None ):
        """Create a new document and load the scene."""
        # Check if ok to continue, return if the user cancelled
        if not self._CheckForSave():
            return

        # Create new document from file path and load it
        if filePath is None:
            
            # Get the start directory. This will be the current working 
            # directory if the project is not set.
            scnsDirPath = self.app.project.GetScenesDirectory()
            if scnsDirPath is None:
                scnsDirPath = os.getcwd()
                
            filePath = wxUtils.FileOpenDialog( 'Open Scene', WILDCARD_SCENE,
                                               defaultDir=scnsDirPath )
            
        # Create new document
        if filePath:
            self.app.CreateScene( filePath )
            self.app.doc.Load()
        
    def OnFileSave( self, evt, saveAs=False ):
        """Save the document."""
        # Set a file path for the document if one does not exist, or for save
        # as
        if self.app.doc.contents.filePath is None or saveAs:

            # Query a new save path
            filePath = self._GetSavePath()
            if filePath:
                self.app.doc.contents.filePath = filePath
            else:
                return
        
        # Save the file
        self.app.doc.Save()
        
    def OnFileSaveAs( self, evt ):
        """
        Call save using the saveAs flag in order to bring up a new dialog box
        so the user may set an alternate save path.
        """
        self.OnFileSave( evt, True )
        
    def OnFileImport( self, evt ):
        """Import assets to project."""
        filePaths = wxUtils.FileOpenDialog( 'Import Models', WILDCARD_MODEL, 
                                            wx.MULTIPLE )
        if filePaths:
            for filePath in filePaths:
                self.app.project.ImportAsset( filePath )
            
    def OnFileNewProject( self, evt ):
        """Build project directory and set project."""
        dirPath = wxUtils.DirDialog( 'Set New Project Directory' )
        if dirPath:
            self.app.project.New( dirPath )
            self.SetProjectPath( dirPath )
            self.app.doc.OnRefresh()
        
    def OnFileSetProject( self, evt ):
        """
        Set the active project directory path and rebuild the resources panel.
        """
        dirPath = wxUtils.DirDialog( 'Set Project Directory' )
        if dirPath:
            self.SetProjectPath( dirPath )
            self.app.doc.OnRefresh()
            
    def OnFileBuildProject( self, evt ):
        """Build the current project to a p3d file."""
        filePath = wxUtils.FileSaveDialog( 'Build Project', WILDCARD_P3D )
        if filePath:
            self.app.project.Build( filePath )
            
    def OnSingleCommand( self, evt ):
        id = evt.GetId()
        fn = self.actns[id]
        fn()
        
    def OnEngagePhysics( self, evt ):
        wrpr = base.game.nodeMgr.Wrap( base.scene.physicsWorld )
        if base.scene.physicsTask not in taskMgr.getAllTasks():
            wrpr.EnablePhysics()
        else:
            wrpr.DisablePhysics()
            
    def OnViewGrid( self, evt ):
        """
        Show or hide the grid based on the checked value of the menu item.
        """
        checked = evt.Checked()
        if checked:
            self.app.grid.show()
        else:
            self.app.grid.hide()
            
    def OnViewCamera( self, evt, yaw_pitch ):
        """ 
        Orbit camera top or bottom by manipulating delta values 
        See p3d.camera.Orbit for more 
        """ 
        delta = pm.Vec2( -base.edCamera.getH() + yaw_pitch[0], -base.edCamera.getP() + yaw_pitch[1] ) 
        base.edCamera.Orbit( delta ) 
        
    def OnCreate( self, evt, typeStr ):
        self.app.AddComponent( typeStr )
        
    def OnCreateActor( self, evt ):
        """
        Turn the selection into actors. This is still a massive hack - we need
        a more concise way of storing this information.
        """
        comps = []
        for np in self.app.selection.nps:
            wrpr = base.game.nodeMgr.Wrap( np )
            modelPath = base.project.GetRelModelPath( np.node().getFullpath() )
            
            wrprCls = base.game.nodeMgr.nodeWrappers['Actor']
            wrpr = wrprCls.Create( modelPath=modelPath )
            wrpr.data.setTransform( np.getTransform() )
            wrpr.SetDefaultValues()
            wrpr.SetParent( wrpr.GetDefaultParent() )
            cmds.Replace( np, wrpr.data )
        
    def OnCreatePrefab( self, evt ):
        """
        Create a new prefab for the selected object in the prefab directory.
        """
        np = self.app.selection.nps[0]
        dirPath = self.app.project.GetPrefabsDirectory()
        assetName = self.app.project.GetUniqueAssetName( 'prefab.xml', dirPath )
        assetPath = os.path.join( dirPath, assetName )
        base.game.scnParser.Save( np, assetPath )
        
    def OnCreateCgShader( self, evt ):
        """
        
        """
        self.app.project.CreateCgShader()
        
    def OnCreateGlslShader( self, evt ):
        """
        
        """
        self.app.project.CreateGlslShader()

    def OnShowHidePane( self, evt ):
        """
        Show or hide the pane based on the menu item that was (un)checked.
        """
        pane = self.paneDefs[evt.GetId()][0]
        self._mgr.GetPane( pane ).Show( evt.Checked() )
        
        # Make sure to call or else we won't see any changes
        self._mgr.Update()
        
    def OnXformSetActiveGizmo( self, evt ):
        if evt.GetId() == ID_XFORM_WORLD:
            self.app.SetGizmoLocal( not evt.Checked() )
            return
            
        arg = None
        if evt.GetId() == ID_XFORM_POS:
            arg = 'pos'
        elif evt.GetId() == ID_XFORM_ROT:
            arg = 'rot'
        elif evt.GetId() == ID_XFORM_SCL:
            arg = 'scl'
        self.app.SetActiveGizmo( arg )
        
    def OnLayout( self, evt ):
        if evt.GetId() == ID_LAYOUT_GAME:
            base.LayoutGameView()
        elif evt.GetId() == ID_LAYOUT_EDITOR:
            base.LayoutEditorView()
        elif evt.GetId() == ID_LAYOUT_BOTH:
            base.LayoutBothView()
        
    def OnUpdateWindowMenu( self, evt ):
        """
        Set the checks in the window menu to match the visibility of the 
        panes.
        """
        def UpdateWindowMenu():
            
            # Check those menus representing panels which are still shown
            # after the event
            for id in self.paneDefs:
                pane = self.paneDefs[id][0]
                if self.mWind.FindItemById( id ) and self._mgr.GetPane( pane ).IsShown():
                    self.mWind.Check( id, True )
                    
        # Uncheck all menus
        for id in self.paneDefs:
            if self.mWind.FindItemById( id ):
                self.mWind.Check( id, False )
        
        # Call after or IsShown() won't return a useful value 
        wx.CallAfter( UpdateWindowMenu )
        
    def OnUpdate( self, msg ):
        """
        Change the appearance and states of buttons on the form based on the
        state of the loaded document.
        
        NOTE: Don't use freeze / thaw as this will cause the 3D viewport to
        flicker.
        """
        self.OnUpdateFile( msg )
        self.OnUpdateEdit( msg )
        self.OnUpdateModify( msg )
        self.OnUpdateView( msg )
        self.OnUpdateProject( msg )
        self.OnUpdateXform( msg )
        
        # Set the frame's title to include the document's file path, include
        # dirty 'star'
        title = ''.join( [FRAME_TITLE, ' - ', self.app.doc.title] )
        if self.app.doc.dirty:
            title += ' *'
        self.SetTitle( title )
        
        self.app.game.pluginMgr.OnUpdate( msg )
        
    def OnUpdateFile( self, msg ):
        """
        Update the file menu. Disable all menu and toolbar items then turn 
        those back on depending on the document's state.
        """
        self.mFile.EnableAllTools( False )
        self.tbFile.EnableAllTools( False )
        
        self.mFile.Enable( ID_FILE_NEW, True )
        self.mFile.Enable( ID_FILE_OPEN, True )
        self.mFile.Enable( ID_FILE_SAVE_AS, True )
        self.mFile.Enable( ID_FILE_PROJ, True )
        self.tbFile.EnableTool( ID_FILE_NEW, True )
        self.tbFile.EnableTool( ID_FILE_OPEN, True )
        self.tbFile.EnableTool( ID_FILE_SAVE_AS, True )
        
        if self.app.doc.dirty:
            self.mFile.Enable( ID_FILE_SAVE, True )
            self.tbFile.EnableTool( ID_FILE_SAVE, True )
        if self.app.project.path is not None:
            self.mFile.Enable( ID_FILE_IMPORT, True )
        
        self.tbFile.Refresh()
        
    def OnUpdateEdit( self, msg ):
        """
        Update the edit menu. Disable undo or redo queus if they are empty
        and make sure to refresh the toolbar.
        """
        val = len( self.app.actnMgr.undoList ) > 0
        self.mEdit.Enable( ID_EDIT_UNDO, val )
        self.tbEdit.EnableTool( ID_EDIT_UNDO, val )
        
        val = len( self.app.actnMgr.redoList ) > 0
        self.mEdit.Enable( ID_EDIT_REDO, val )
        self.tbEdit.EnableTool( ID_EDIT_REDO, val )
        
        self.tbEdit.Refresh()
        
    def OnUpdateModify( self, msg ):
        self.tbModify.EnableTool( ID_MODIFY_PHYSICS, False )
        if base.scene.physicsWorld is not None:
            self.tbModify.EnableTool( ID_MODIFY_PHYSICS, True )
            
            if base.scene.physicsTask not in taskMgr.getAllTasks():
                self.tbModify.ToggleTool( ID_MODIFY_PHYSICS, False )
            else:
                self.tbModify.ToggleTool( ID_MODIFY_PHYSICS, True )
                
        self.tbModify.Refresh()
        
    def OnUpdateView( self, msg ):
        """
        Update the view menu. Ensure the grid menu item's checked state 
        matches the visibility of the grid.
        """
        self.mView.Check( ID_VIEW_GRID, False )
        if not self.app.grid.isHidden():
            self.mView.Check( ID_VIEW_GRID, True )
        
    def OnUpdateProject( self, msg ):
        self.mProj.EnableAllTools( False )
        
        self.mProj.Enable( ID_PROJ_NEW, True )
        self.mProj.Enable( ID_PROJ_SET, True )
        
        if self.app.project.path is not None:
            self.mProj.EnableAllTools( True )
            
    def OnUpdateXform( self, msg ):
        gizmo = self.app.gizmoMgr.GetActiveGizmo()
        if gizmo is None:
            self.tbXform.ToggleTool( ID_XFORM_SEL, True )
        elif gizmo.getName() == 'pos':
            self.tbXform.ToggleTool( ID_XFORM_POS, True )
        elif gizmo.getName() == 'rot':
            self.tbXform.ToggleTool( ID_XFORM_ROT, True )
        elif gizmo.getName() == 'scl':
            self.tbXform.ToggleTool( ID_XFORM_SCL, True )
        
        val = not self.app.gizmoMgr.GetGizmoLocal( 'pos' )
        self.tbXform.ToggleTool( ID_XFORM_WORLD, val )
            
        self.tbXform.Refresh()
        
    def OnMove( self, evt ):
        """
        Keep the window's position on hand before it gets maximized as this is
        the number we need to save to preferences.
        """
        if not self.IsMaximized():
            self.preMaxPos = self.GetPosition()
        
    def OnSize( self, evt ):
        """
        Keep the window's size on hand before it gets maximized as this is the
        number we need to save to preferences.
        """
        if not self.IsMaximized():
            self.preMaxSize = self.GetSize()
        
    def SetProjectPath( self, dirPath ):
        """
        Set the project path and rebuild the resources panel.
        """
        self.app.project.Set( dirPath )
        self.pnlRsrcs.Build( self.app.project.path )
        
    def BuildFileActions( self ):
        """Add tools, set long help strings and bind toolbar events."""
        commonActns = [
            ActionItem( 'New', os.path.join( 'data', 'images', 'document.png' ), self.OnFileNew, ID_FILE_NEW ),
            ActionItem( 'Open', os.path.join( 'data', 'images', 'folder-horizontal-open.png' ), self.OnFileOpen, ID_FILE_OPEN ),
            ActionItem( 'Save', os.path.join( 'data', 'images', 'disk-black.png' ), self.OnFileSave, ID_FILE_SAVE ),
            ActionItem( 'Save As', os.path.join( 'data', 'images', 'disk-black-pencil.png' ), self.OnFileSaveAs, ID_FILE_SAVE_AS ),
        ]
        
        # Create file menu
        self.mFile = CustomMenu()
        self.mFile.AppendActionItems( commonActns, self )
        self.mFile.AppendSeparator()
        self.mFile.AppendActionItem( ActionItem( 'Import...', '', self.OnFileImport, ID_FILE_IMPORT ), self )
        
        # Create project actions as a submenu
        self.mProj = CustomMenu()
        actns = [
            ActionItem( 'New...', '', self.OnFileNewProject, ID_PROJ_NEW ),
            ActionItem( 'Set...', '', self.OnFileSetProject, ID_PROJ_SET ),
            ActionItem( 'Build...', '', self.OnFileBuildProject, ID_PROJ_BUILD )
        ]
        self.mProj.AppendActionItems( actns, self )
        self.mFile.AppendMenu( ID_FILE_PROJ, '&Project', self.mProj )
        
        # Create file toolbar
        self.tbFile = CustomAuiToolBar( self, -1, style=wx.aui.AUI_TB_DEFAULT_STYLE )
        self.tbFile.SetToolBitmapSize( TBAR_ICON_SIZE )
        self.tbFile.AppendActionItems( commonActns )
        self.tbFile.Realize()
        
    def BuildEditActions( self ):
        """Add tools, set long help strings and bind toolbar events."""
        commonActns = [
            ActionItem( 'Undo', os.path.join( 'data', 'images', 'arrow-curve-flip.png' ), self.OnSingleCommand, ID_EDIT_UNDO ),
            ActionItem( 'Redo', os.path.join( 'data', 'images', 'arrow-curve.png' ), self.OnSingleCommand, ID_EDIT_REDO )
        ]
        
        grpActns = [
            ActionItem( 'Group', '', self.OnSingleCommand, ID_EDIT_GROUP ),
            ActionItem( 'Ungroup', '', self.OnSingleCommand, ID_EDIT_UNGROUP )
        ]
        
        pntActns = [
            ActionItem( 'Parent', '', self.OnSingleCommand, ID_EDIT_PARENT ),
            ActionItem( 'Unparent', '', self.OnSingleCommand, ID_EDIT_UNPARENT )
        ]
        
        # Create edit menu
        self.mEdit = CustomMenu()
        self.mEdit.AppendActionItems( commonActns, self )
        self.mEdit.AppendSeparator()
        self.mEdit.AppendActionItems( grpActns, self )
        #self.mEdit.AppendSeparator()
        #self.mEdit.AppendActionItems( pntActns, self )
        
        # Create edit toolbar
        self.tbEdit = CustomAuiToolBar( self, -1, style=wx.aui.AUI_TB_DEFAULT_STYLE )
        self.tbEdit.SetToolBitmapSize( TBAR_ICON_SIZE )
        self.tbEdit.AppendActionItems( commonActns )
        self.tbEdit.Realize()
        
    def BuildModifyActions( self ):
        """Add tools, set long help strings and bind toolbar events."""
        actns = [
            ActionItem( 'Engage Physics', os.path.join( 'data', 'images', 'point.png' ), self.OnEngagePhysics, ID_MODIFY_PHYSICS, kind=wx.ITEM_CHECK )
        ]
        
        # Create edit menu
        self.mModify = CustomMenu()
        self.mModify.AppendActionItems( actns, self )
        
        # Create edit toolbar
        self.tbModify = CustomAuiToolBar( self, -1, style=wx.aui.AUI_TB_DEFAULT_STYLE )
        self.tbModify.SetToolBitmapSize( TBAR_ICON_SIZE )
        self.tbModify.AppendActionItems( actns )
        self.tbModify.Realize()
        
    def BuildXformActions( self ):
        """Add tools, set long help strings and bind toolbar events."""
        fn = self.OnXformSetActiveGizmo
        actns = [
            ActionItem( 'Select', os.path.join( 'data', 'images', 'select.png' ), fn, ID_XFORM_SEL, kind=wx.ITEM_RADIO ),
            ActionItem( 'Move', os.path.join( 'data', 'images', 'move.png' ), fn, ID_XFORM_POS, kind=wx.ITEM_RADIO ),
            ActionItem( 'Rotate', os.path.join( 'data', 'images', 'rotate.png' ), fn, ID_XFORM_ROT, kind=wx.ITEM_RADIO ),
            ActionItem( 'Scale', os.path.join( 'data', 'images', 'scale.png' ), fn, ID_XFORM_SCL, kind=wx.ITEM_RADIO ),
            ActionItem( 'World Transform', os.path.join( 'data', 'images', 'globe.png' ), fn, ID_XFORM_WORLD, kind=wx.ITEM_CHECK )
        ]
        
        # Create xform toolbar
        self.tbXform = CustomAuiToolBar( self, -1, style=wx.aui.AUI_TB_DEFAULT_STYLE )
        self.tbXform.SetToolBitmapSize( TBAR_ICON_SIZE )
        self.tbXform.AddSpacer( 0 )   # Need to insert a null object here or the radio buttons don't seem to work (win7 at least).
        self.tbXform.AppendActionItems( actns )
        self.tbXform.Realize()
        
    def BuildLayoutActions( self ):
        """Add tools, set long help strings and bind toolbar events."""
        actns = [
            ActionItem( 'Editor', os.path.join( 'data', 'images', 'application-sidebar-list.png' ), self.OnLayout, ID_LAYOUT_EDITOR, kind=wx.ITEM_RADIO ),
            ActionItem( 'Game', os.path.join( 'data', 'images', 'layout-game.png' ), self.OnLayout, ID_LAYOUT_GAME, kind=wx.ITEM_RADIO ),
            ActionItem( 'Both', os.path.join( 'data', 'images', 'layout-both.png' ), self.OnLayout, ID_LAYOUT_BOTH, kind=wx.ITEM_RADIO )
        ]
        
        # Create layout toolbar
        self.tbLayout = CustomAuiToolBar( self, -1, style=wx.aui.AUI_TB_DEFAULT_STYLE )
        self.tbLayout.SetToolBitmapSize( TBAR_ICON_SIZE )
        self.tbLayout.AddSpacer( 0 )   # Need to insert a null object here or the radio buttons don't seem to work (win7 at least).
        self.tbLayout.AppendActionItems( actns )
        self.tbLayout.ToggleTool( ID_LAYOUT_EDITOR, True )
        self.tbLayout.Realize()
                
    def BuildViewMenu( self ):
        """Build the view menu."""
        viewActns = [
            ActionItem( 'Grid', '', self.OnViewGrid, ID_VIEW_GRID, kind=wx.ITEM_CHECK )
        ]
        
        camActns = [ 
            ActionItem( 'Top', '', self.OnViewCamera, ID_VIEW_TOP, args=(0, -90) ), 
            ActionItem( 'Bottom', '', self.OnViewCamera, ID_VIEW_BOTTOM, args=(0, 90) ), 
            ActionItem( 'Left', '', self.OnViewCamera, ID_VIEW_LEFT, args=(-90, 0) ), 
            ActionItem( 'Right', '', self.OnViewCamera, ID_VIEW_RIGHT, args=(90, 0) ), 
            ActionItem( 'Front', '', self.OnViewCamera, ID_VIEW_FRONT, args=(0, 0) ), 
            ActionItem( 'Back', '', self.OnViewCamera, ID_VIEW_BACK, args=(-180, 0) )
        ] 
        self.mCameras = CustomMenu() 
        self.mCameras.AppendActionItems( camActns, self ) 

        # Append to view menu 
        self.mView = CustomMenu()
        self.mView.AppendActionItems( viewActns, self )
        self.mView.AppendSeparator() 
        self.mView.AppendSubMenu( self.mCameras, '&Camera' ) 
                
    def BuildCreateMenu( self ):
        """Build the create menu."""
        lightActns = [
            ActionItem( 'Ambient', '', self.OnCreate, args='AmbientLight' ),
            ActionItem( 'Point', '', self.OnCreate, args='PointLight' ),
            ActionItem( 'Directional', '', self.OnCreate, args='DirectionalLight' ),
            ActionItem( 'Spot', '', self.OnCreate, args='Spotlight' )
        ]
        mLights = CustomMenu()
        mLights.AppendActionItems( lightActns, self )
        
        mCollActns = [
            ActionItem( 'Node', '', self.OnCreate, args='CollisionNode' ),
            ActionItem( 'Box', '', self.OnCreate, args='CollisionBox' ),
            ActionItem( 'Ray', '', self.OnCreate, args='CollisionRay' ),
            ActionItem( 'Sphere', '', self.OnCreate, args='CollisionSphere' ),
            ActionItem( 'Inverse Sphere', '', self.OnCreate, args='CollisionInvSphere' ),
            ActionItem( 'Tube', '', self.OnCreate, args='CollisionTube' )
        ]
        mColl = CustomMenu()
        mColl.AppendActionItems( mCollActns, self )
        
        texActns = [
            ActionItem( 'Texture', '', self.OnCreate, args='Texture' )#,
            #ActionItem( 'Texture Stage', '', self.OnCreate, args='TextureStage' )
        ]
        mTex = CustomMenu()
        mTex.AppendActionItems( texActns, self )
        
        shaActns = [
            ActionItem( 'Shader', '', self.OnCreate, args='Shader' )
        ]
        mSha = CustomMenu()
        mSha.AppendActionItems( shaActns, self )
        
        bltActions = [
            ActionItem( 'World', '', self.OnCreate, args='BulletWorld' ),
            ActionItem( 'Debug Node', '', self.OnCreate, args='BulletDebugNode' ),
            ActionItem( 'Rigid Body Node', '', self.OnCreate, args='BulletRigidBodyNode' ),
            ActionItem( 'Character Controller Node', '', self.OnCreate, args='BulletCharacterControllerNode' ),
            #ActionItem( 'Capsule Shape', '', self.OnCreate, args='BulletCapsuleShape' ),
            ActionItem( 'Box Shape', '', self.OnCreate, args='BulletBoxShape' ),
            ActionItem( 'Plane Shape', '', self.OnCreate, args='BulletPlaneShape' )
        ]
        mBlt = CustomMenu()
        mBlt.AppendActionItems( bltActions, self )
        
        self.mCreate = CustomMenu()
        self.mCreate.AppendActionItem( ActionItem( 'Panda Node', '', self.OnCreate, args='PandaNode' ), self )
        self.mCreate.AppendActionItem( ActionItem( 'Actor', '', self.OnCreateActor ), self )
        self.mCreate.AppendSubMenu( mColl, '&Collision' )
        self.mCreate.AppendSubMenu( mLights, '&Lights' )
        self.mCreate.AppendSubMenu( mTex, '&Texture' )
        self.mCreate.AppendSubMenu( mSha, '&Shader' )
        self.mCreate.AppendSubMenu( mBlt, '&Bullet' )
        self.mCreate.AppendSeparator()
        self.mCreate.AppendActionItem( ActionItem( 'Prefab', '', self.OnCreatePrefab ), self )
        #self.mCreate.AppendSeparator()
        #self.mCreate.AppendActionItem( ActionItem( 'Cg Shader', '', self.OnCreateCgShader ), self )
        #self.mCreate.AppendActionItem( ActionItem( 'Glsl Shader', '', self.OnCreateGlslShader ), self )
        
    def BuildWindowMenu( self ):
        """Build show / hide controls for panes."""
        self.mWind = wx.Menu()
        for id, paneDef in self.paneDefs.items():
            if paneDef[1]:
                self.mWind.AppendCheckItem( id, paneDef[2].caption )
                self.Bind( wx.EVT_MENU, self.OnShowHidePane, id=id )
        self.mb.Append( self.mWind, '&Window' )
                
    def RebuildWindowMenu( self ):
        self.Freeze()
        index = self.mb.FindMenu( 'Window' )
        self.mb.Remove( index )
        self.BuildWindowMenu()
        self.OnUpdateWindowMenu( None )
        self.Thaw()
        
    def BuildMenuBar( self ):
        """Build the menu bar and attach all menus to it."""
        self.mb.Append( self.mFile, '&File' )
        self.mb.Append( self.mEdit, '&Edit' )
        self.mb.Append( self.mView, '&View' )
        self.mb.Append( self.mCreate, '&Create' )
        
        self.SetMenuBar( self.mb )
        
    def BuildAuiManager( self ):
        """
        Define the behaviour for each aui manager panel, then add them to the
        manager.
        """
        # Define aui manager panes
        # Each tuple is defined as: widget, show in window menu, aui panel 
        # info
        self.paneDefs = {
            ID_WIND_FILE_TOOLBAR:(self.tbFile, True,
                wx.aui.AuiPaneInfo()
                .Name( 'tbFile' )
                .Caption( 'File Toolbar' )
                .ToolbarPane()
                .Top()),
                
            ID_WIND_EDIT_TOOLBAR:(self.tbEdit, True,
                wx.aui.AuiPaneInfo()
                .Name( 'tbEdit' )
                .Caption( 'Edit Toolbar' )
                .ToolbarPane()
                .Top()),
                
            ID_WIND_MODIFY_TOOLBAR:(self.tbModify, True,
                wx.aui.AuiPaneInfo()
                .Name( 'tbModify' )
                .Caption( 'Modify Toolbar' )
                .ToolbarPane()
                .Top()),
                
            ID_WIND_XFORM_TOOLBAR:(self.tbXform, True,
                wx.aui.AuiPaneInfo()
                .Name( 'tbXform' )
                .Caption( 'Transform Toolbar' )
                .ToolbarPane()
                .Top()),
                
            ID_WIND_LAYOUT_TOOLBAR:(self.tbLayout, True,
                wx.aui.AuiPaneInfo()
                .Name( 'tbLayout' )
                .Caption( 'Layout Toolbar' )
                .ToolbarPane()
                .Top()),

            ID_WIND_VIEWPORT:(self.pnlViewport, False,
                wx.aui.AuiPaneInfo()
                .Name( 'pnlViewport' )
                .Caption( 'Viewport' )
                .CloseButton( False )
                .MaximizeButton( True )
                .Center()),
                
            ID_WIND_SCENE_GRAPH:(self.pnlSceneGraph, True,
                wx.aui.AuiPaneInfo()
                .Name( 'pnlSceneGraph' )
                .Caption( 'Scene Graph' )
                .CloseButton( True )
                .MaximizeButton( True )
                .MinSize( (100, 100) )
                .Left()
                .Position( 2 )),
                
            ID_WIND_LIGHT_LINKER:(self.pnlLightLinker, True,
                wx.aui.AuiPaneInfo()
                .Name( 'pnlLightLinker' )
                .Caption( 'Light Linker' )
                .CloseButton( True )
                .MaximizeButton( True )
                .MinSize( (100, 100) )
                .Right()
                .Position( 2 )),
                
            ID_WIND_RESOURCES:(self.pnlRsrcs, True,
                wx.aui.AuiPaneInfo()
                .Name( 'pnlRsrcs' )
                .Caption( 'Resources' )
                .CloseButton( True )
                .MaximizeButton( True )
                .MinSize( (100, 100) )
                .Right()
                .Position( 2 )),
                
            ID_WIND_PROPERTIES:(self.pnlProps, True,
                wx.aui.AuiPaneInfo()
                .Name( 'pnlProps' )
                .Caption( 'Properties' )
                .CloseButton( True )
                .MaximizeButton( True )
                .MinSize( (100, 100) )
                .Right()),
                
            ID_WIND_LOG:(self.pnlLog, True,
                wx.aui.AuiPaneInfo()
                .Name( 'pnlLog' )
                .Caption( 'Log' )
                .CloseButton( True )
                .MaximizeButton( True )
                .MinSize( (100, 100) )
                .Bottom()
                .Position( 1 ))
        }
                        
        # Build aui manager and add each pane
        self._mgr = wx.aui.AuiManager( self )
        for paneDef in self.paneDefs.values():
            self._mgr.AddPane( paneDef[0], paneDef[2] )
        
        # Bind aui manager events
        self._mgr.Bind( wx.aui.EVT_AUI_PANE_CLOSE, self.OnUpdateWindowMenu )
        
        # Create config and load preferences for all panels
        self.auiCfg = AuiManagerConfig( self._mgr, 'pandaEditorWindow' )
        self.auiCfg.Load()
        self._mgr.Update()