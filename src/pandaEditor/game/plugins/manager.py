from yapsy.PluginManager import PluginManager


class Manager(PluginManager):

    def __init__(self, base, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.base = base

    def on_init(self):
        for plugin in self.getAllPlugins():
            print('Loaded pluging:', plugin.plugin_object)
            plugin.plugin_object.on_init(self.base)
