import logging

from plugins import base


logger = logging.getLogger(__name__)


class ExamplePlugin(base.Base):

    def on_update(self, base, comps):
        # logger.info(self, 'on_update')
        pass

    def on_scene_close(self, base):
        # logger.info(self, 'on_scene_close')
        pass

    def on_project_modified(self, base, file_paths):
        # logger.info(self, 'on_project_modified')
        pass