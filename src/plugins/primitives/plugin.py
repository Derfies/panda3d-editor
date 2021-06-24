import logging
import os

import p3d
import panda3d.core as pc
import wx

from direct.showbase.PythonUtil import getBase as get_base
from pandaEditor.plugins import base
from pandaEditor.ui.createdialog import CreateDialog
from wxExtra import utils as wxutils


logger = logging.getLogger(__name__)


ID_CREATE_BOX = wx.NewId()
ID_CREATE_CONE = wx.NewId()
ID_CREATE_CYLINDER = wx.NewId()
ID_CREATE_SPHERE = wx.NewId()


class PrimitivesPlugin(base.Base):

    def on_init(self):

        # Build primitives menu.
        m_prim = wx.Menu()
        m_prim.Append(ID_CREATE_BOX, '&Box')
        m_prim.Append(ID_CREATE_CONE, '&Cone')
        m_prim.Append(ID_CREATE_CYLINDER, '&Cylinder')
        m_prim.Append(ID_CREATE_SPHERE, '&Sphere')

        # Bind primitives menu events.
        ui = get_base().frame
        wxutils.IdBind(ui, wx.EVT_MENU, ID_CREATE_BOX, self.on_create_box)
        wxutils.IdBind(ui, wx.EVT_MENU, ID_CREATE_CONE, self.on_create_cone)
        wxutils.IdBind(ui, wx.EVT_MENU, ID_CREATE_CYLINDER, self.on_create_cylinder)
        wxutils.IdBind(ui, wx.EVT_MENU, ID_CREATE_SPHERE, self.on_create_sphere)

        # Append to create menu
        ui.mCreate.AppendSeparator()
        ui.mCreate.AppendSubMenu(m_prim, '&Primitives')

    def create_geometry(self, name, geom):
        dir_path = get_base().project.models_directory
        asset_name = get_base().project.get_unique_asset_name(
            f'{name}.bam',
            dir_path
        )
        asset_path = os.path.join(dir_path, asset_name)
        geom.write_bam_file(pc.Filename.from_os_specific(asset_path))
        logger.info(f'Wrote bam file: {asset_path}')

        # Add the new model to the scene.
        # TODO: This is duplicated from viewport, so maybe do further
        # abstraction there.
        rel_path = get_base().project.get_project_relative_path(asset_path)
        logging.info(f'Adding model: {rel_path}')
        get_base().add_component('ModelRoot', fullpath=rel_path)

    def on_create(self, primitive, props, geom_fn):
        dialog = CreateDialog(
            f'Create {primitive} Primitive',
            props,
            wx.GetApp().GetTopWindow(),
            title='Create Primitive Model',
        )
        dialog.CenterOnParent()
        if dialog.ShowModal() == wx.ID_OK:
            geom = geom_fn(**dialog.GetValues())
            self.create_geometry(primitive.lower(), pc.NodePath(geom))

    def on_create_box(self, evt):
        props = {
            'width': 1,
            'height': 1,
            'depth': 1,
            'origin': pc.Point3(0, 0, 0),
            'flip_normals': False,
        }
        self.on_create('box', props, p3d.geometry.box)

    def on_create_cone(self, evt):
        props = {
            'radius': 1.0,
            'height': 2.0,
            'num_segs': 16,
            'degrees': 360,
            'axis': pc.Vec3(0, 0, 1),
            'origin': pc.Point3(0, 0, 0),
        }
        self.on_create('cone', props, p3d.geometry.cone)

    def on_create_cylinder(self, evt):
        props = {
            'radius': 1.0,
            'height': 2.0,
            'num_segs': 16,
            'degrees': 360,
            'axis': pc.Vec3(0, 0, 1),
            'origin': pc.Point3(0, 0, 0),
        }
        self.on_create('cylinder', props, p3d.geometry.cylinder)

    def on_create_sphere(self, evt):
        props = {
            'radius': 1.0,
            'num_segs': 16,
            'degrees': 360,
            'axis': pc.Vec3(0, 0, 1),
            'origin': pc.Point3(0, 0, 0),
        }
        self.on_create('sphere', props, p3d.geometry.sphere)
