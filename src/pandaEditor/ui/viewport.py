import logging
import os

from direct.showbase.PythonUtil import getBase as get_base

from p3d.wxPanda import Viewport as WxViewport
from dragdroptarget import DragDropTarget


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
        
    def get_dropped_object(self, x, y):
        x, y = self.screen_to_viewport(x, y)
        np = self.base.selection.get_node_path_at_position(x, y)
        return get_base().node_manager.wrap(np)

    def drag_drop_validate(self, x, y, data):
        drags = []
        for elem in data:
            drags.append((
                isinstance(elem, str) and
                os.path.splitext(elem)[1] in self.asset_handlers
            ))
        return all(drags)

    def on_drop(self, x, y, data):
        for file_path in data:
            ext = os.path.splitext(file_path)[1]
            handler = self.asset_handlers[ext]
            handler(file_path, x, y)

    def add_model(self, file_path, x, y):
        logging.info(f'Adding model: {file_path}')
        self.base.add_component('ModelRoot', model_path=file_path)

    def add_particles(self, file_path, x, y):
        logging.info(f'Adding particle: {file_path}')
        self.base.add_component('ParticleEffect', config_path=file_path)

    def add_prefab(self, file_path, x, y):
        logging.info(f'Adding prefab: {file_path}')
        self.base.add_prefab(file_path)

    def add_texture(self, file_path, x, y):
        logging.info(f'Adding texture: {file_path}')
        tex_comp = self.base.add_component('Texture', filename=file_path)
        drop_comp = self.get_dropped_object(x, y)

        # TODO: Need to wrap this with a command so it can be undone.
        drop_comp.texture = tex_comp
