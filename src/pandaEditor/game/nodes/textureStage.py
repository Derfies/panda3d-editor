import pandac.PandaModules as pm
from pandac.PandaModules import TextureStage as TS

from base import Base
from attributes import Attribute as Attr


class TextureStage( Base ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', TS )
        Base.__init__( self, *args, **kwargs )
        
        self.initArgs = ['textureStage']
        
        pAttr = Attr( 'Texture Stage' )
        pAttr.children.extend( 
            [
                Attr( 'Name', str, TS.getName, TS.setName )
            ]
        )
        self.attributes.append( pAttr )