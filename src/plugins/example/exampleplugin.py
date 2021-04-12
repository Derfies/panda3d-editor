from editor.plugins import base


class ExamplePlugin(base.Base):

    def on_update(self, base, comps):
        print(self, 'on_update')

    def on_scene_close(self, base):
        print(self, 'on_scene_close')

    def on_project_modified(self, base):
        print(self, 'on_project_modified')
