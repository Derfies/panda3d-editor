import panda3d.core as pm
from panda3d.core import Spotlight as SL

from .light import Light
from .lensNode import LensNode
from .attributes import NodeAttribute as Attr


class Spotlight( Light, LensNode ):
    
    type_ = SL
    
    def __init__( self, *args, **kwargs ):
        LensNode.__init__( self, *args, **kwargs )
        Light.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Attenuation', pm.Vec3, SL.getAttenuation, SL.setAttenuation ),
            Attr( 'Exponent', float, SL.getExponent, SL.setExponent ),
            Attr( 'Specular Color', pm.Vec4, SL.getSpecularColor, SL.setSpecularColor ),
            Attr( 'Shadow Caster', bool, SL.isShadowCaster, SL.setShadowCaster ),
            parent='Spotlight'
        )