import logging
import os
import pickle

import wx

from pandaEditor import commands as cmds
from pandaEditor import constants


logger = logging.getLogger(__name__)


class DragDropManager:

    def __init__(self, base):
        self.base = base
        self.dragComps = []

        # Define file types and their actions.
        self.fileTypes = {}
        for model_extn in constants.MODEL_EXTENSIONS:
            self.fileTypes[model_extn] = self.add_model
        # self.fileTypes = {
        #     '.egg': self.AddModel,
        #     '.bam': self.AddModel,
        #     '.pz': self.AddModel,
        #     '.sha': self.AddShader,
        #     #'.png':self.AddTexture,
        #     #'.tga':self.AddTexture,
        #     #'.jpg':self.AddTexture
        # }

    def DoFileDrop(self, filePath, np):
        ext = os.path.splitext(filePath)[1]
        if ext in self.fileTypes:
            fn = self.fileTypes[ext]
            fn(filePath, np)

    def Start(self, src, dragComps, data):
        self.dragComps = dragComps

        # Create a custom data object that we can drop onto the toolbar
        # which contains the tool's id as a string
        do = wx.CustomDataObject('NodePath')
        do.SetData(pickle.dumps(data))

        # Create the drop source and begin the drag and drop operation
        ds = wx.DropSource(src)
        ds.SetData(do)
        ds.DoDragDrop(True)

        # Clear drag node paths
        self.dragComps = []

    def ValidateDropItem(self, x, y, parent):
        dropComp = parent.GetDroppedObject(x, y)
        #if dropComp is None:
        if len(self.dragComps) == 1:
            try:
                filePath = self.dragComps[0]
                ext = os.path.splitext(filePath)[1]
                #print 'in: ',  ext in self.fileTypes
                return ext in self.fileTypes
            except Exception:
                pass
                #print e
                #return False
        #return False

        wrpr = base.node_manager.wrap(dropComp)
        if wx.GetMouseState().CmdDown():
            return wrpr.validate_drag_drop(self.dragComps, dropComp)
        else:
            return wrpr.get_possible_connections(self.dragComps)

    def OnDropItem(self, str, parent, x, y):

        # Get the item at the drop point
        dropComp = parent.GetDroppedObject(x, y)
        if len(self.dragComps) == 1:
            try:
                filePath = self.dragComps[0]
                self.DoFileDrop(filePath, dropComp)
            except:
                raise
        if dropComp is None:
            return
        wrpr = self.base.node_manager.wrap(dropComp)
        self.data = {}
        dragComps = self.base.dDropMgr.dragComps
        if wx.GetMouseState().CmdDown():
            wrpr.on_drag_drop(dragComps, wrpr.data)
        else:
            menu = wx.Menu()
            for cnnctn in wrpr.get_possible_connections(dragComps):
                mItem = wx.MenuItem(menu, wx.NewId(), cnnctn.label)
                menu.AppendItem(mItem)
                menu.Bind(wx.EVT_MENU, self.OnConnect, id=mItem.GetId())
                self.data[mItem.GetId()] = cnnctn
            parent.PopupMenu(menu)
            menu.Destroy()

    def OnConnect(self, evt):
        dragComps = self.base.dDropMgr.dragComps
        cnnctn = self.data[evt.get_id()]
        cmds.Connect(dragComps, cnnctn, cnnctn.connect)

    def add_model(self, file_path, np=None):
        self.base.AddComponent('ModelRoot', model_path=file_path)

    def AddShader(self, filePath, np=None):
        wrpr = self.base.node_manager.wrap(np)
        prop = wrpr.find_property('shader')
        cmds.SetAttribute([np], [prop], filePath)

    def AddTexture(self, filePath, np=None):
        pandaPath = pm.Filename.fromOsSpecific(filePath)

        theTex = None
        if pm.TexturePool.hasTexture(pandaPath):
            logger.info('found in pool')
            for tex in pm.TexturePool.findAllTextures():
                if tex.getFilename() == pandaPath:
                    theTex = tex

        # Try to find it in the scene.
        #for foo in base.scene.comps.keys():
        #    print type(foo) , ' : ', foo
        logger.info(theTex)
        if theTex is not None and theTex in base.scene.comps.keys():
            logger.info('found in scene')
            if np is not None:
                npWrpr = base.node_manager.wrap(np)
                npWrpr.find_property('texture').Set(theTex)

        else:

            logger.info('creating new')
            wrpr = self.AddComponent('Texture')
            #wrpr = base.node_manager.Wrap(loader.loadTexture(pandaPath))
            #wrpr.SetDefaultValues()
            #wrpr.SetParent(wrpr.GetDefaultParent())
            wrpr.find_property('fullPath').Set(pandaPath)
            #pm.TexturePool.addTexture(wrpr.data)

            if np is not None:
                npWrpr = base.node_manager.wrap(np)
                npWrpr.find_property('texture').Set(wrpr.data)
