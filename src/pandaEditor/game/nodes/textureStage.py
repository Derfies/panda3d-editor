import pandac.PandaModules as pm
from pandac.PandaModules import TextureStage as TS

from base import Base
from attributes import Attribute as Attr


class TextureStage( Base ):
    
    type_ = TS
    initArgs = ['textureStage']
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Name', str, TS.getName, TS.setName ),
            parent='TextureStage'
        )