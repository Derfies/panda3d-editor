import logging

from game.plugins.base import Base as GamePluginBase
from game.plugins.manager import Manager as GameManager
from pandaEditor.plugins.base import Base as EditorPluginBase


logger = logging.getLogger(__name__)


class Manager(GameManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCategoriesFilter({
            'editor': EditorPluginBase,
            'game': GamePluginBase,
        })

    def getPluginsOfCategory(self, category_name):
        try:
            return super().getPluginsOfCategory(category_name)
        except KeyError:
            logger.error('Failed to resolve plugin categories', exc_info=True)
            return []

    def on_init(self):
        super().on_init()
        for plugin in self.getAllPlugins():
            logger.info(f'Loaded plugin: {plugin.name}')

    def on_update(self, comps):
        for plugin in self.getPluginsOfCategory('editor'):
            plugin.plugin_object.on_update(comps)

    def on_scene_close(self):
        for plugin in self.getPluginsOfCategory('editor'):
            plugin.plugin_object.on_scene_close()

    def on_project_modified(self, file_paths):
        for plugin in self.getPluginsOfCategory('editor'):
            plugin.plugin_object.on_project_modified(file_paths)

    def on_build_ui(self):
        for plugin in self.getPluginsOfCategory('editor'):
            plugin.plugin_object.on_build_ui()
