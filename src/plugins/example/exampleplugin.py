from plugins import base


class ExamplePlugin(base.Base):

    def on_update(self, base, comps):
        # print(self, 'on_update')
        pass

    def on_scene_close(self, base):
        # print(self, 'on_scene_close')
        pass

    def on_project_modified(self, base, file_paths):
        # print(self, 'on_project_modified')
        pass