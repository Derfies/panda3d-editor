import panda3d.core as pm
from panda3d.core import TextureStage as TS

from .base import Base
from .attributes import Attribute as Attr


class TextureStage( Base ):
    
    type_ = TS
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Name', str, TS.getName, TS.setName ),
            parent='TextureStage'
        )