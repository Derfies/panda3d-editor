import panda3d.core as pm
from panda3d.bullet import BulletPlaneShape as BPS

from game.nodes.manager import import_wrapper


Base = import_wrapper('nodes.base.Base')
Attr = import_wrapper('nodes.attributes.Attribute')


class BulletPlaneShape(Base):
    
    type_ = BPS
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            Attr('Normal', pm.Vec3, initDefault=pm.Vec3(0, 0, 1)),
            Attr('Constant', int, initDefault=0),
            parent='BulletBoxShape'
        )