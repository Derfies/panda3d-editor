import logging

from pandaEditor.plugins import base


logger = logging.getLogger(__name__)


class ExampleEditorPlugin(base.Base):

    def on_init(self):
        # logger.info('on_init')
        pass

    def on_update(self, comps):
        # logger.info(f'on_update {comps}')
        pass

    def on_scene_close(self):
        # logger.info('on_scene_close')
        pass

    def on_project_modified(self, file_paths):
        # logger.info(f'on_project_modified {file_paths}')
        pass