import panda3d.core as pc
from pandac.PandaModules import Texture as T

from .base import Base
from .attributes import Attribute as Attr


class Texture( Base ):
    
    type_ = T
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Name', str, T.getName, T.setName, initDefault='' ),
            Attr( 'Full Path', pc.Filename, T.getFullpath, self.SetTex ),
            parent='Texture'
        )
        
    def SetTex( self, data, filePath ):
        try:
            pandaPath = pc.Filename.fromOsSpecific( filePath )
        except TypeError:
            pandaPath = filePath
        data.setFullpath( pandaPath )
        data.setup2dTexture()
        data.read( pandaPath ) 