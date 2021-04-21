from direct.showbase.PythonUtil import getBase as get_base


class Connection:

    def __set__(self, instance, value):
        super().__set__(instance, value)
        if value is not None:
            get_base().scene.register_connection(instance, value, self.name)
        
    def clear(self, value):
        super().clear(value)
        get_base().scene.deregister_connection(value)
