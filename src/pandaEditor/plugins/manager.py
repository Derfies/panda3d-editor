import logging

from game.plugins.manager import Manager as GameManager


logger = logging.getLogger(__name__)


class Manager(GameManager):

    def getPluginsOfCategory(self, category_name):
        try:
            return super().getPluginsOfCategory(category_name)
        except KeyError:
            return []

    # def on_init(self):
    #     super().on_init()
    #
    #     logger.info(f'Loading plugins')
    #     for plugin in self.getAllPlugins():
    #         logger.info(f'Loaded plugin: {plugin.name}')

    def on_update(self, comps):
        for plugin in self.getPluginsOfCategory('editor'):
            plugin.plugin_object.on_update(self.base, comps)

    def on_scene_close(self):
        for plugin in self.getPluginsOfCategory('editor'):
            plugin.plugin_object.on_scene_close(self.base)

    def on_project_modified(self, file_paths):
        for plugin in self.getPluginsOfCategory('editor'):
            plugin.plugin_object.on_project_modified(self.base, file_paths)
