from direct.showbase.PythonUtil import getBase as get_base


class Connection:

    def __set__(self, instance, value):
        super().__set__(instance, value)

        # TODO: This possibly should register when set then deregister when
        # set to None.
        if value is not None:
            get_base().scene.register_connection(instance, value, self.name)
        
    def clear(self, value):

        # Possibly on the wrong class - move to Connections class.
        super().clear(value)
        get_base().scene.deregister_connection(value)
