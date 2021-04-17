from direct.showbase.PythonUtil import getBase as get_base


class SceneRoot:
    
    def get_children(self):
        comps = (
            get_base().render2d,
            get_base().render
        ) + tuple(get_base().scene.comps.keys())
        return [
            get_base().node_manager.wrap(comp)
            for comp in comps
        ]
