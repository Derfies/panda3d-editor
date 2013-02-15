import panda3d.core as pc
import pandac.PandaModules as pm
from panda3d.core import Filename
from pandac.PandaModules import Texture as T

from base import Base
from attributes import Attribute as Attr


class Texture( Base ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', T )
        Base.__init__( self, *args, **kwargs )
        
        self.initArgs = ['texture']
        
        pAttr = Attr( 'Texture' )
        pAttr.children.extend( 
            [
                Attr( 'Name', str, T.getName, T.setName ),
                Attr( 'Full Path', Filename, T.getFullpath, self.SetTex )
            ]
        )
        self.attributes.append( pAttr )
        
    def SetTex( self, data, filePath ):
        try:
            pandaPath = pc.Filename.fromOsSpecific( filePath )
        except TypeError:
            pandaPath = filePath
        data.setFullpath( pandaPath )
        data.setup2dTexture()
        data.read( pandaPath ) 