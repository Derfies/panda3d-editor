from game.nodes.camera import Camera
from game.nodes.wrappermeta import WrapperMeta


class BaseCam(Camera, metaclass=WrapperMeta):

    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(base.cam)
        wrpr.SetupNodePath()
        return wrpr
