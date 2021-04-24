import logging
import os
import pickle

import wx
from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor import commands as cmds
from pandaEditor import constants


logger = logging.getLogger(__name__)


class DragDropManager:

    def __init__(self, base):
        self.base = base
        self.drag_comps = []

        # Define file types and their actions.
        self.file_types = {
            model_extn: self.add_model
            for model_extn in constants.MODEL_EXTENSIONS
        }
        self.file_types['.ptf'] = self.add_particles
        self.file_types['.xml'] = self.add_prefab   # Conflicts with scene xml
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
        if ext in self.file_types:
            fn = self.file_types[ext]
            fn(filePath, np)

    def start(self, src, drag_comps, data):
        logging.info(f'Starty drag drop: {drag_comps} -> {data}')
        self.drag_comps = drag_comps

        # TODO: Figure out why a component doesn't pickle properly.
        do = wx.CustomDataObject('NodePath')
        do.SetData(pickle.dumps(data))

        # Create the drop source and begin the drag and drop operation.
        ds = wx.DropSource(src)
        ds.SetData(do)
        ds.DoDragDrop(True)

        # Clear drag node paths.
        self.drag_comps = []

    def ValidateDropItem(self, x, y, parent):
        dropComp = parent.GetDroppedObject(x, y)
        if len(self.drag_comps) == 1:
            try:
                filePath = self.drag_comps[0]
                ext = os.path.splitext(filePath)[1]
                return ext in self.file_types
            except Exception as e:
                logger.warning(str(e))

        wrpr = base.node_manager.wrap(dropComp)
        if wx.GetMouseState().CmdDown():
            return wrpr.validate_drag_drop(self.drag_comps, dropComp)
        else:
            return wrpr.get_possible_connections(self.drag_comps)

    def OnDropItem(self, str, parent, x, y):

        # Get the item at the drop point
        dropComp = parent.GetDroppedObject(x, y)
        if len(self.drag_comps) == 1:
            try:
                filePath = self.drag_comps[0]
                self.DoFileDrop(filePath, dropComp)
            except:
                raise
        if dropComp is None:
            return
        wrpr = self.base.node_manager.wrap(dropComp)
        self.data = {}
        dragComps = self.base.drag_drop_manager.drag_comps
        if wx.GetMouseState().CmdDown():
            wrpr.on_drag_drop(dragComps, wrpr.data)
        else:
            menu = wx.Menu()
            print('dragComps:', dragComps)
            for cnnctn in wrpr.get_possible_connections(dragComps):
                mItem = wx.MenuItem(menu, wx.NewId(), cnnctn.label)
                menu.AppendItem(mItem)
                menu.Bind(wx.EVT_MENU, self.OnConnect, id=mItem.GetId())
                self.data[mItem.GetId()] = cnnctn
            parent.PopupMenu(menu)
            menu.Destroy()

    def OnConnect(self, evt):
        dragComps = self.base.drag_drop_manager.drag_comps
        cnnctn = self.data[evt.get_id()]
        cmds.connect(dragComps, cnnctn, cnnctn.connect)

    def add_model(self, file_path, np=None):
        logging.info(f'Adding model: {file_path}')
        self.base.AddComponent('ModelRoot', model_path=file_path)

    def add_particles(self, file_path, np=None):
        logging.info(f'Adding particle: {file_path}')
        self.base.AddComponent('ParticleEffect', config_path=file_path)

    def add_prefab(self, file_path, np=None):
        self.base.add_prefab(file_path)
        # np = self.base.selection.node_paths[0]ge
        # dir_path = self.base.project.GetPrefabsDirectory()
        # asset_name = self.base.project.GetUniqueAssetName('prefab.xml', dir_path)
        # asset_path = os.path.join(dir_path, asset_name)
        # root_comp = get_base().node_manager.wrap(get_base().render)
        # get_base().scene_parser.load(file_path, root_comp)

    # def AddShader(self, filePath, np=None):
    #     wrpr = self.base.node_manager.wrap(np)
    #     prop = wrpr.find_property('shader')
    #     cmds.set_attribute([np], [prop], filePath)
    #
    # def AddTexture(self, filePath, np=None):
    #     pandaPath = pm.Filename.fromOsSpecific(filePath)
    #
    #     theTex = None
    #     if pm.TexturePool.hasTexture(pandaPath):
    #         logger.info('found in pool')
    #         for tex in pm.TexturePool.findAllTextures():
    #             if tex.getFilename() == pandaPath:
    #                 theTex = tex
    #
    #     # Try to find it in the scene.
    #     #for foo in base.scene.comps.keys():
    #     #    print type(foo) , ' : ', foo
    #     logger.info(theTex)
    #     if theTex is not None and theTex in base.scene.comps.keys():
    #         logger.info('found in scene')
    #         if np is not None:
    #             npWrpr = base.node_manager.wrap(np)
    #             npWrpr.find_property('texture').Set(theTex)
    #
    #     else:
    #
    #         logger.info('creating new')
    #         wrpr = self.AddComponent('Texture')
    #         #wrpr = base.node_manager.Wrap(loader.loadTexture(pandaPath))
    #         #wrpr.SetDefaultValues()
    #         #wrpr.SetParent(wrpr.GetDefaultParent())
    #         wrpr.find_property('fullPath').Set(pandaPath)
    #         #pm.TexturePool.addTexture(wrpr.data)
    #
    #         if np is not None:
    #             npWrpr = base.node_manager.wrap(np)
    #             npWrpr.find_property('texture').Set(wrpr.data)
