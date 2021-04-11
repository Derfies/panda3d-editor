from panda3d.core import TextureStage as TS

from game.nodes.manager import import_wrapper


Base = import_wrapper('nodes.base.Base')
Attr = import_wrapper('nodes.attributes.Attribute')


class TextureStage(Base):
    
    type_ = TS
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            Attr('Name', str, TS.getName, TS.setName),
            parent='TextureStage'
        )
