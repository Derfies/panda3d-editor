from direct.showbase.PythonUtil import getBase as get_base
from yapsy.IPlugin import IPlugin


class IBase(IPlugin):

    def on_init(self):
        pass

    def register_node_wrapper(self, type_str, cls):
        get_base().game.node_manager.wrappers[type_str] = cls
