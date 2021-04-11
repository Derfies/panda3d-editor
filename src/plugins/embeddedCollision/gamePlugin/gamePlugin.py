from .constants import *
from game.plugins.base import Base


class GamePlugin(Base):
    
    def __init__(self, *args):
        Base.__init__(self, *args, sort=-10)
        
    def OnInit(self):
        from embeddedCollision import EmbeddedCollision
        from embeddedBulletTriangleMeshShape import EmbeddedBulletTriangleMeshShape

        self.RegisterNodeWrapper(TAG_EMBEDDED_COLLISION, EmbeddedCollision)
        self.RegisterNodeWrapper(TAG_EMBEDDED_BULLET_TRIANGLE_MESH_SHAPE, EmbeddedBulletTriangleMeshShape)