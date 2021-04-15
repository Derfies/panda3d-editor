from direct.showbase.PythonUtil import getBase as get_base


class SceneRoot:
    
    def GetChildren(self):
        comps = (
            get_base().render2d,
            get_base().render
        ) + tuple(get_base().scene.comps.keys())
        return [
            get_base().node_manager.Wrap(comp)
            for comp in comps
        ]