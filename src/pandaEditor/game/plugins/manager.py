from yapsy.PluginManager import PluginManager


class Manager(PluginManager):

    def on_init(self):
        for plugin in self.getAllPlugins():
            plugin.plugin_object.on_init()
