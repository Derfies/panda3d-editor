from panda3d.bullet import BulletCapsuleShape as BCS, ZUp

from game.nodes.manager import import_wrapper


Base = import_wrapper('nodes.base.Base')
Attr = import_wrapper('nodes.attributes.Attribute')


class BulletCapsuleShape(Base):
    
    type_ = BCS
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            Attr('Radius', float, BCS.getRadius, initDefault=0.5),
            Attr('Height', float, BCS.getHalfHeight, initDefault=1),
            Attr('Up', int, initDefault=ZUp),
            parent='BulletCapsuleShape'
        )
