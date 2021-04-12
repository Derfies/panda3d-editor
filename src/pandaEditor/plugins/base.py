from game.plugins.base import Base as GameBase


class Base(GameBase):

    def on_update(self, base, comps):
        pass

    def on_scene_close(self, base):
        pass

    def on_project_modified(self, base, file_paths):
        pass
