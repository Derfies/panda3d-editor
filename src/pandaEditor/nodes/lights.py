from direct.showbase.PythonUtil import getBase as get_base


class Light:
    
    def set_default_values(self):
        super().set_default_values()

        # Automatically set render to use this light.
        render = get_base().node_manager.wrap(get_base().render)
        render.lights.append(self)
