from direct.showbase.PythonUtil import getBase as get_base


class SceneRoot:

    # TODO: Move to game class?
    @property
    def children(self):
        return [
            get_base().node_manager.wrap(data)
            for data in [
                get_base().render2d,
                get_base().render,
            ] + list(get_base().scene.objects.keys())
        ]
