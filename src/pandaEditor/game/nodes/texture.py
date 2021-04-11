import panda3d.core as pc
from panda3d.core import Texture as T

from game.nodes.manager import import_wrapper


Base = import_wrapper('nodes.base.Base')
Attr = import_wrapper('nodes.attributes.Attribute')


class Texture(Base):
    
    type_ = T
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            Attr('Name', str, T.getName, T.setName, initDefault=''),
            Attr('Full Path', pc.Filename, T.getFullpath, self.SetTex),
            parent='Texture'
        )
        
    def SetTex(self, data, filePath):
        try:
            pandaPath = pc.Filename.fromOsSpecific(filePath)
        except TypeError:
            pandaPath = filePath
        data.setFullpath(pandaPath)
        data.setup2dTexture()
        data.read(pandaPath)
