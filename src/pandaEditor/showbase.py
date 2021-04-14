import panda3d.core as pc
from direct.directtools.DirectGrid import DirectGrid
from direct.showbase import ShowBaseGlobal
from pubsub import pub

import p3d
from p3d.displayShading import DisplayShading
from p3d.editorCamera import EditorCamera
from p3d.frameRate import FrameRate
from p3d.mouse import MOUSE_ALT
from pandaEditor.ui.mainFrame import MainFrame
from pandaEditor import actions, commands, gizmos
from pandaEditor.assetManager import AssetManager
from pandaEditor.dragDropManager import DragDropManager
from scene import Scene
from pandaEditor.project import Project
from pandaEditor.selection import Selection
from pandaEditor.ui.document import Document
from pandaEditor.game.plugins.base import Base as GamePluginBase
from pandaEditor.game.showbase import ShowBase as GameShowBase
from pandaEditor.nodes.manager import Manager as NodeManager
from pandaEditor.plugins.manager import Manager as PluginManager
from pandaEditor.plugins.base import Base as EditorPluginBase
from pandaEditor.sceneParser import SceneParser


class ShowBase(GameShowBase):

    node_manager_cls = NodeManager
    plug_manager_cls = PluginManager
    scene_parser_cls = SceneParser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.forcedAspectWins = []

        self.startWx()
        self.frame = MainFrame(self, None, size=(800, 600))
        self.frame.Show()
        self.frame.pnlViewport.Initialize()

        self.gizmo = False
        self._xformTask = None

        # Bind publisher events
        pub.subscribe(self.OnUpdate, 'Update')

        self.SetupEdRender()
        self.SetupEdRender2d()
        self.SetupEdMouseWatcher()
        self.SetupEdCamera()

        # Make additional camera for 2d nodes
        cam2d = self.makeCamera2d(self.win)
        cam2d.reparentTo(self.edRender2d)

        # Add the editor window, camera and pixel 2d to the list of forced
        # aspect windows so aspect is fixed when the window is resized.
        self.forcedAspectWins.append((self.win, self.edCamera, self.edPixel2d))

        self.Reset()

        # Create project manager
        self.project = Project(self)
        self.frame.SetProjectPath(self.frame.cfg.Read('projDirPath'))

        # Create grid
        self.SetupGrid()

        # Create frame rate meter
        self.frameRate = FrameRate()

        # Create shading mode keys
        dsp = DisplayShading()
        dsp.accept('4', dsp.Wireframe)
        dsp.accept('5', dsp.Shade)
        dsp.accept('6', dsp.Texture)

        # Set up gizmos
        self.SetupGizmoManager()

        # Bind mouse events
        self.accept('mouse1', self.OnMouse1Down)
        self.accept('shift-mouse1', self.OnMouse1Down, [True])
        self.accept('control-mouse1', self.OnMouse1Down)
        self.accept('mouse2', self.OnMouse2Down)
        self.accept('mouse1-up', self.OnMouse1Up)
        self.accept('mouse2-up', self.OnMouse2Up)

        # Create selection manager
        self.selection = Selection(
            self,
            camera=self.edCamera,
            root2d=self.edRender2d,
            win=self.win,
            mouseWatcherNode=self.edMouseWatcherNode
        )

        # Create our managers.
        self.assetMgr = AssetManager(self)
        self.dDropMgr = DragDropManager(self)
        self.actnMgr = actions.Manager()

        # Bind events
        self.accept('z', self.Undo)
        self.accept('shift-z', self.Redo)
        self.accept('f', self.FrameSelection)
        self.accept('del', lambda fn: commands.Remove(fn()),
                    [self.selection.Get])
        self.accept('backspace', lambda fn: commands.Remove(fn()),
                    [self.selection.Get])
        self.accept('control-d', lambda fn: commands.Duplicate(fn()),
                    [self.selection.Get])
        self.accept('control-g', lambda fn: commands.Group(fn()),
                    [self.selection.Get])
        self.accept('control-s', self.frame.OnFileSave, [None])
        self.accept('arrow_up', lambda fn: commands.Select(fn()),
                    [self.selection.SelectParent])
        self.accept('arrow_down', lambda fn: commands.Select(fn()),
                    [self.selection.SelectChild])
        self.accept('arrow_left', lambda fn: commands.Select(fn()),
                    [self.selection.SelectPrev])
        self.accept('arrow_right', lambda fn: commands.Select(fn()),
                    [self.selection.SelectNext])
        self.accept('projectFilesModified', self.OnProjectFilesModified)

        # Create a "game"
        # self.game = EditorBase(self)

        self.load_plugins()

        # Start with a new scene
        self.CreateScene()
        self.doc.OnRefresh()

        self.windowEvent(None)

    def load_plugins(self):
        # self.plugin_manager.setCategoriesFilter({
        #     'editor': EditorPluginBase,
        #     'game': GamePluginBase,
        # })
        super().load_plugins()

    def SetupEdRender(self):
        """
        Create editor root node behind render node so we can keep editor only
        nodes out of the scene.
        """
        self.edRender = pc.NodePath('edRender')
        render.reparentTo(self.edRender)

    def SetupEdRender2d(self):
        """
        Creates the render2d scene graph, the primary scene graph for 2-d
        objects and gui elements that are superimposed over the 3-d geometry
        in the window.
        """
        self.edRender2d = pc.NodePath('edRender2d')

        # Set up some overrides to turn off certain properties which we
        # probably won't need for 2-d objects.
        self.edRender2d.setDepthTest(0)
        self.edRender2d.setDepthWrite(0)
        self.edRender2d.setMaterialOff(1)
        self.edRender2d.setTwoSided(1)

        # This special root, pixel2d, uses units in pixels that are relative
        # to the window. The upperleft corner of the window is (0, 0),
        # the lowerleft corner is (xsize, -ysize), in this coordinate system.
        xsize, ysize = self.getSize()
        self.edPixel2d = self.edRender2d.attachNewNode(pc.PGTop('edPixel2d'))
        self.edPixel2d.setPos(-1, 0, 1)
        if xsize > 0 and ysize > 0:
            self.edPixel2d.setScale(2.0 / xsize, 1.0, 2.0 / ysize)

    def SetupEdMouseWatcher(self):

        # Setup mouse watcher for the editor window
        buttonThrowers, pointerWatcherNodes = self.setupMouseCB(self.win)
        self.edMouseWatcher = buttonThrowers[0].getParent()
        self.edMouseWatcherNode = self.edMouseWatcher.node()
        self.edMouseWatcherParent = self.edMouseWatcher.getParent()

    def SetupEdCamera(self):

        # Create editor camera
        self.edCamera = EditorCamera(
            'camera',
            style=p3d.camera.CAM_VIEWPORT_AXES,
            speed=0.5,
            pos=(56, 56, 42),
            rootNp=self.edRender,
            rootP2d=self.edPixel2d,
            win=self.win,
            mouseWatcherNode=self.edMouseWatcherNode
       )
        self.edCamera.reparentTo(self.edRender)
        self.edCamera.Start()

        # Modify the existing display region and create a new one for the
        # editor camera.
        self.dr = self.cam.node().getDisplayRegion(0)
        self.dr.setClearColorActive(True)
        self.dr.setClearColor(self.getBackgroundColor())
        self.dr.setActive(False)
        self.dr.setSort(20)

        self.dr2d = self.cam2d.node().getDisplayRegion(0)
        self.dr2d.setActive(False)
        self.dr2d.setSort(21)

        self.edDr = self.win.makeDisplayRegion(0, 1, 0, 1)
        self.edDr.setCamera(self.edCamera)
        self.edDr.setClearColorActive(True)
        self.edDr.setClearColor((0.63, 0.63, 0.63, 0))

    def windowEvent(self, *args, **kwargs):
        """
        Overridden so as to fix the aspect ratio of the editor camera and
        editor pixel2d.
        """
        super().windowEvent(*args, **kwargs)

        for win, cam, pixel2d in self.forcedAspectWins:
            aspectRatio = self.getAspectRatio(win)
            cam.node().getLens().setAspectRatio(aspectRatio)

            # Fix pixel2d scale for new window size
            # Temporary hasattr for old Pandas
            if not hasattr(win, 'getSbsLeftXSize'):
                pixel2d.setScale(2.0 / win.getXSize(), 1.0, 2.0 / win.getYSize())
            else:
                pixel2d.setScale(2.0 / win.getSbsLeftXSize(), 1.0, 2.0 / win.getSbsLeftYSize())

    def GetEditorRenderMasks(self):
        """
        Return the show, hide and clear masks for objects that are to be
        rendered only in the editor viewport.
        """
        show = pc.BitMask32()
        show.setRangeTo(True, 28, 4)
        hide = pc.BitMask32().allOn()
        hide.setRangeTo(False, 28, 4)
        clear = pc.BitMask32()

        return show, hide, clear

    def SetupCameraMask(self):
        """
        Set camera mask to draw all objects but those with the first four bits
        flipped. All editor geometry will use these bits so as to not be
        rendered in the game view.
        """
        bits = self.cam.node().getCameraMask()
        bits.setRangeTo(False, 28, 4)
        self.cam.node().setCameraMask(bits)

        # Set edRender mask
        self.edRender.node().adjustDrawMask(*self.GetEditorRenderMasks())

    def SetupRenderMask(self):
        """
        Set the draw mask for the render node to be visible to all cameras.
        Since we are adjusting the draw mask of the render node's parent we
        need to manually set this node's mask or it will inherit those
        properties.
        """
        showMask = pc.BitMask32().allOn()
        hideMask = pc.BitMask32()
        clearMask = pc.BitMask32()
        render.node().adjustDrawMask(showMask, hideMask, clearMask)

    def Reset(self):


        """Remove all default nodes and recreate them."""
        # Remove all default nodes and set them to None so they are recreated
        # properly.
        for name in ('cam', 'camera', 'cam2d', 'camera2d'):
            np = getattr(self, name)
            np.removeNode()
            setattr(self, name, None)

        # Set up render and render2d again, forcing their new values into
        # builtins.
        self.setupRender()

        # This is kinda lame imho. These default nodes are created by importing
        # the showbase global module, which makes it difficult to recreate these
        # nodes for our purposes.
        render2d = pc.NodePath('render2d')
        aspect2d = render2d.attachNewNode(pc.PGTop('aspect2d'))
        ShowBaseGlobal.render2d = render2d
        ShowBaseGlobal.aspect2d = aspect2d
        self.setupRender2d()

        __builtins__['render'] = self.render
        __builtins__['render2d'] = self.render2d
        __builtins__['aspect2d'] = self.aspect2d
        __builtins__['pixel2d'] = self.pixel2d

        self.makeCamera(self.win)
        self.makeCamera2d(self.win)
        __builtins__['camera'] = self.camera

        for cam, dr in {self.cam:self.dr, self.cam2d:self.dr2d}.items():
            defaultDr = cam.node().getDisplayRegion(0)
            self.win.removeDisplayRegion(defaultDr)
            dr.setCamera(cam)

        # Set up masks
        self.SetupCameraMask()
        self.SetupRenderMask()

        # Set auto shader.
        render.setShaderAuto()

    def ResetModelPath(self):
        """
        Clears the model path, making sure to restore the current working
        directory (so editor models can still be found).
        """
        pc.getModelPath().clear()
        pc.getModelPath().prependDirectory('.')

    def DisableEditorMouse(self):
        self.edMouseWatcher.detachNode()

    def EnableEditorMouse(self):
        self.edMouseWatcher.reparentTo(self.edMouseWatcherParent)

    def LayoutGameView(self):
        """Deactivate both display regions and enable mouse."""
        self.DisableEditorMouse()

        self.dr.setActive(True)
        self.dr.setDimensions(0, 1, 0, 1)
        self.dr2d.setActive(True)
        self.dr2d.setDimensions(0, 1, 0, 1)

        self.edRender2d.hide()
        self.edPixel2d.hide()

    def LayoutEditorView(self):
        """Deactivate both display regions and enable mouse."""
        self.EnableEditorMouse()

        self.dr.setActive(False)
        self.dr2d.setActive(False)

        self.edDr.setActive(True)
        self.edRender2d.show()
        self.edPixel2d.show()

    def LayoutBothView(self):
        """Deactivate both display regions and enable mouse."""
        self.EnableEditorMouse()

        self.dr.setActive(True)
        self.dr.setDimensions(0.65, 1, 0.65, 1)

        self.dr2d.setActive(True)
        self.dr2d.setDimensions(0.65, 1, 0.65, 1)

        self.edDr.setActive(True)
        self.edRender2d.show()
        self.edPixel2d.show()

    def SetupGrid(self):
        """Create the grid and set up its appearance."""
        self.grid = DirectGrid(
            gridSize=20.0,
            gridSpacing=1.0,
            planeColor=(0.5, 0.5, 0.5, 0.0),
            parent=self.edRender
       )
        self.grid.snapMarker.hide()
        self.grid.centerLines.setColor((0, 0, 0, 0))
        self.grid.centerLines.setThickness(2)
        self.grid.majorLines.setColor((0.25, 0.25, 0.25, 0))
        self.grid.majorLines.setThickness(1)
        self.grid.minorLines.setColor((0.5, 0.5, 0.5, 0))
        self.grid.updateGrid()

    def SetupGizmoManager(self):
        """Create gizmo manager."""
        gizmoMgrRootNp = self.edRender.attachNewNode('gizmoManager')
        kwargs = {
            'camera':self.edCamera,
            'rootNp':gizmoMgrRootNp,
            'win':self.win,
            'mouseWatcherNode':self.edMouseWatcherNode
        }
        self.gizmoMgr = gizmos.Manager(**kwargs)
        self.gizmoMgr.AddGizmo(gizmos.Translation('pos', **kwargs))
        self.gizmoMgr.AddGizmo(gizmos.Rotation('rot', **kwargs))
        self.gizmoMgr.AddGizmo(gizmos.Scale('scl', **kwargs))

        # Bind gizmo manager events
        self.accept('q', self.SetActiveGizmo, [None])
        self.accept('w', self.SetActiveGizmo, ['pos'])
        self.accept('e', self.SetActiveGizmo, ['rot'])
        self.accept('r', self.SetActiveGizmo, ['scl'])
        self.accept('space', self.ToggleGizmoLocal)
        self.accept('+', self.gizmoMgr.SetSize, [2])
        self.accept('-', self.gizmoMgr.SetSize, [0.5])

    def SetActiveGizmo(self, name):
        self.gizmoMgr.SetActiveGizmo(name)
        self.frame.OnUpdateXform(None)

    def SetGizmoLocal(self, val):
        self.gizmoMgr.SetLocal(val)
        self.frame.OnUpdateXform(None)

    def ToggleGizmoLocal(self):
        self.gizmoMgr.ToggleLocal()
        self.frame.OnUpdateXform(None)

    def OnMouse1Down(self, shift=False):
        """
        Handle mouse button 1 down event. Start the drag select operation if
        a gizmo is not being used and the alt key is not down, otherwise start
        the transform operation.
        """
        if (
            not self.gizmoMgr.IsDragging() and
            MOUSE_ALT not in self.edCamera.mouse.modifiers
        ):
            self.selection.StartDragSelect(shift)
        elif self.gizmoMgr.IsDragging():
            self.StartTransform()

    def OnMouse2Down(self):
        """
        Handle mouse button 2 down event. Start the transform operation if a
        gizmo is being used.
        """
        if self.gizmoMgr.IsDragging():
            self.StartTransform()

    def OnMouse1Up(self):
        """
        Handle mouse button 1 up event. Stop the drag select operation if the
        marquee is running, otherwise stop the transform operation if a gizmo
        is being used.
        """
        if self.selection.marquee.IsRunning():
            commands.Select(self.selection.StopDragSelect())
        elif self.gizmoMgr.IsDragging() or self.gizmo:
            self.StopTransform()

    def OnMouse2Up(self):
        """
        Handle mouse button 2 up event. Stop the transform operation if a
        gizmo is being used.
        """
        if self.gizmoMgr.IsDragging() or self.gizmo:
            self.StopTransform()

    def StartTransform(self):
        """
        Start the transfrom operation by adding a task to constantly send a
        selection modified message while transfoming.
        """
        self.gizmo = True
        self._xformTask = taskMgr.add(self.doc.OnSelectionModified,
                                       'SelectionModified')

    def StopTransform(self):
        """
        Stop the transfrom operation by removing the selection modified
        message task. Also create a transform action and push it onto the undo
        queue.
        """
        # Remove the transform task
        if self._xformTask in taskMgr.getAllTasks():
            taskMgr.remove(self._xformTask)
            self._xformTask = None

        actGizmo = self.gizmoMgr.GetActiveGizmo()
        actns = []
        for i, np in enumerate(actGizmo.attachedNps):
            actns.append(actions.Transform(np, np.getTransform(), actGizmo.initNpXforms[i]))
        actn = actions.Composite(actns)
        self.actnMgr.Push(actn)
        self.gizmo = False

        # Make sure to mark the NodePath as dirty in case it is a child of a
        # model root.
        wrpr = self.node_manager.Wrap(np)
        wrpr.SetModified(True)

        # Call OnModified next frame. Not sure why but if we call it straight
        # away it causes a small jitter when xforming...
        taskMgr.doMethodLater(0, self.doc.OnModified, 'dragDrop',
                               [actGizmo.attachedNps])

    def FrameSelection(self):
        """
        Call frame selection on the camera if there are some node paths in the
        selection.
        """
        nps = self.selection.GetNodePaths()
        if nps:
            self.edCamera.Frame(nps)
        else:
            self.edCamera.Frame([self.scene.rootNp])

    def OnUpdate(self, comps=None):
        """
        Subscribed to the update selection message. Make sure that the
        selected nodes are attached to the managed gizmos, then refresh the
        active one.
        """
        nps = self.selection.GetNodePaths()
        self.gizmoMgr.AttachNodePaths(nps)
        self.gizmoMgr.RefreshActiveGizmo()
        self.selection.Update()

    def CreateScene(self, filePath=None, newDoc=True):
        """
        Create an empty scene and set its root node to the picker's root node.
        """
        # Reset undo queue if creating a new document
        if newDoc:
            self.actnMgr.Reset()

        # Close the current scene if there is one
        self.selection.Clear()
        if hasattr(self, 'scene'):
            self.scene.Close()

        # Create a new scene
        self.scene = Scene()
        self.scene.rootNp.reparentTo(self.edRender)

        # Set the selection and picker root node to the scene's root node
        self.selection.rootNp = self.scene.rootNp
        self.selection.picker.rootNp = self.scene.rootNp
        self.selection.marquee.rootNp = self.scene.rootNp

        # Create the document wrapper if creating a new document
        if newDoc:
            self.doc = Document(filePath, self.scene)

    def AddComponent(self, typeStr, *args, **kwargs):
        wrprCls = self.node_manager.GetWrapperByName(typeStr)
        wrpr = wrprCls.Create(*args, **kwargs)
        wrpr.SetDefaultValues()
        wrpr.SetParent(wrpr.GetDefaultParent())

        # Bit of a hack. Sometimes a wrapper can create multiple components
        # when Create is called. Make sure to set default values on all the
        # components that were created.
        if hasattr(wrpr, 'extraNps'):
            for np in wrpr.extraNps:
                eWrpr = self.node_manager.Wrap(np)
                eWrpr.SetDefaultValues()
        commands.Add([wrpr.data])

        return wrpr

    def OnProjectFilesModified(self, filePaths):
        self.assetMgr.OnAssetModified(filePaths)
        self.plugin_manager.on_project_modified(filePaths)

    def Undo(self):
        self.actnMgr.Undo()
        self.doc.OnModified()

    def Redo(self):
        self.actnMgr.Redo()
        self.doc.OnModified()

    def Group(self):
        nps = self.selection.GetNodePaths()
        if nps:
            commands.Group(nps)

    def Ungroup(self):
        nps = self.selection.GetNodePaths()
        if nps:
            commands.Ungroup(nps)

    def Parent(self):
        pass

    def Unparent(self):
        pass
