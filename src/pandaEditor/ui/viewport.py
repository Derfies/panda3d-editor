import logging
import os

from direct.showbase.PythonUtil import getBase as get_base

import pandaEditor.commands as cmds
from dragdroptarget import DragDropTarget
from game.nodes.base import Base
from p3d.wxPanda import Viewport as WxViewport
from wxExtra import CustomMenu, ActionItem


logger = logging.getLogger(__name__)


class Viewport(WxViewport):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        dt = DragDropTarget(
            self.drag_drop_validate,
            self.on_drop
        )
        self.SetDropTarget(dt)

        self.asset_handlers = {
            '.bam': self.add_model,
            '.dae': self.add_model,
            '.egg': self.add_model,
            '.gltf': self.add_model,
            '.obj': self.add_model,
            '.png': self.add_texture,
            '.ptf': self.add_particles,
            '.pz': self.add_model,
            '.xml': self.add_prefab,    # Conflicts with scene xml extn.
        }
        
    def screen_to_viewport(self, x, y):
        x = (x / float(self.GetSize()[0])- 0.5) * 2
        y = (y / float(self.GetSize()[1]) - 0.5) * -2
        return x, y
        
    def get_drop_component(self, x, y):
        x, y = self.screen_to_viewport(x, y)
        np = self.base.selection.get_node_path_at_position(x, y)
        return get_base().node_manager.wrap(np)

    def drag_drop_validate(self, x, y, data):
        """
        Accept strings (assets from the resources panel) or components.

        """
        are_assets = all([isinstance(elem, str) for elem in data])
        are_comps = all([isinstance(elem, Base) for elem in data])
        if not are_assets and not are_comps:
            return False

        if are_assets:
            return all([
                os.path.splitext(elem)[1] in self.asset_handlers
                for elem in data
            ])
        else:
            drop_comp = self.get_drop_component(x, y)
            return drop_comp.get_possible_connections(data)

    def on_drop(self, x, y, data):
        all_assets = all([isinstance(elem, str) for elem in data])
        if all_assets:
            for file_path in data:
                ext = os.path.splitext(file_path)[1]
                handler = self.asset_handlers[ext]
                handler(file_path, x, y)
        else:
            menu = CustomMenu()
            drop_comp = self.get_drop_component(x, y)
            possible_conns = drop_comp.get_possible_connections(data)
            for conn_name, conn in possible_conns.items():
                action = ActionItem(
                    conn_name,
                    '',
                    self.on_connect,
                    args=(data, drop_comp, conn_name)
                )
                menu.AppendActionItem(action, menu)
            self.PopupMenu(menu)
            menu.Destroy()

    def on_connect(self, evt, args):
        drag_comps, drop_comp, conn_name = args
        cmds.set_attribute([drop_comp], conn_name, drag_comps[0])

    def add_model(self, file_path, x, y):
        rel_path = get_base().project.get_project_relative_path(file_path)
        logging.info(f'Adding model: {rel_path}')
        self.base.add_component('ModelRoot', model_path=rel_path)

    def add_particles(self, file_path, x, y):
        logging.info(f'Adding particle: {file_path}')
        self.base.add_component('ParticleEffect', config_path=file_path)

    def add_prefab(self, file_path, x, y):
        logging.info(f'Adding prefab: {file_path}')
        self.base.add_prefab(file_path)

    def add_texture(self, file_path, x, y):
        rel_path = get_base().project.get_project_relative_path(file_path)
        logging.info(f'Adding texture: {rel_path}')
        tex_comp = self.base.add_component('Texture', filename=rel_path)
        drop_comp = self.get_drop_component(x, y)

        # TODO: Need to wrap this with a command so it can be undone.
        drop_comp.texture = tex_comp
