import panda3d.core as pm
from panda3d.bullet import BulletBoxShape as BBS

from game.nodes.manager import import_wrapper


Base = import_wrapper('nodes.base.Base')
Attr = import_wrapper('nodes.attributes.Attribute')


class BulletBoxShape(Base):
    
    type_ = BBS
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            Attr('Half Extents', pm.Vec3, BBS.getHalfExtentsWithMargin, 
                  initDefault=pm.Vec3(0.5, 0.5, 0.5)),
            parent='BulletBoxShape'
        )
