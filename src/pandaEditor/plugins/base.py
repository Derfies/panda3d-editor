from game.plugins.ibase import IBase


class Base(IBase):

    def on_update(self, comps):
        pass

    def on_scene_close(self):
        pass

    def on_project_modified(self, file_paths):
        pass

    def on_build_ui(self):
        pass
