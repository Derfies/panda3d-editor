from game.plugins.manager import Manager as GameManager


class Manager(GameManager):

    def getPluginsOfCategory(self, category_name):
        try:
            return super().getPluginsOfCategory(category_name)
        except KeyError:
            return []

    def on_update(self, comps):
        for plugin in self.getPluginsOfCategory('editor'):
            plugin.plugin_object.on_update(self.base, comps)

    def on_scene_close(self):
        for plugin in self.getPluginsOfCategory('editor'):
            plugin.plugin_object.on_scene_close(self.base)

    def on_project_modified(self):
        for plugin in self.getPluginsOfCategory('editor'):
            plugin.plugin_object.on_project_modified(self.base)
