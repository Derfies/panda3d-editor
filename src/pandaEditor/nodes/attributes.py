from direct.showbase.PythonUtil import getBase as get_base


class Connection:

    def connect(self, value):
        super().connect(value)
        get_base().scene.register_connection(value, self)
        
    def clear(self, value):
        super().clear(value)
        get_base().scene.deregister_connection(value)
