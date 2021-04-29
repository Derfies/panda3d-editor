import logging
import os

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
            '.egg': self.add_model,
            '.bam': self.add_model,
            '.pz': self.add_model,
            '.ptf': self.add_particles,
            '.xml': self.add_prefab,    # Conflicts with scene xml extn.
        }
        
    def screen_to_viewport(self, x, y):
        x = (x / float(self.GetSize()[0])- 0.5) * 2
        y = (y / float(self.GetSize()[1]) - 0.5) * -2
        return x, y
        
    def get_dropped_object(self, x, y):
        x, y = self.screen_to_viewport(x, y)
        return self.base.selection.GetNodePathAtPosition(x, y)

    def drag_drop_validate(self, x, y, data):
        return any([isinstance(elem, str) for elem in data])

    def on_drop(self, x, y, data):
        for file_path in data:
            if not isinstance(file_path, str):
                continue
            ext = os.path.splitext(file_path)[1]
            if ext not in self.asset_handlers:
                continue
            handler = self.asset_handlers[ext]
            handler(file_path)

    def add_model(self, file_path):
        logging.info(f'Adding model: {file_path}')
        self.base.add_component('ModelRoot', model_path=file_path)

    def add_particles(self, file_path):
        logging.info(f'Adding particle: {file_path}')
        self.base.add_component('ParticleEffect', config_path=file_path)

    def add_prefab(self, file_path):
        logging.info(f'Adding prefab: {file_path}')
        self.base.add_prefab(file_path)
