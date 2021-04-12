from game.nodes.camera import Camera
from game.nodes.nodepath import NodePath


class BaseCam(NodePath):

    @classmethod
    def GetDefaultPropertyData(cls):
        return Camera.Create(name='cam').GetPropertyData()
