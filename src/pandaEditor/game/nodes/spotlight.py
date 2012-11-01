import pandac.PandaModules as pm
from pandac.PandaModules import Spotlight as SL

from light import Light
from lensNode import LensNode
from attributes import NodeAttribute as Attr


class Spotlight( Light, LensNode ):
    
    def __init__( self, *args, **kwargs ):
        kwargs['nType'] = SL
        LensNode.__init__( self, *args, **kwargs )
        Light.__init__( self, *args, **kwargs )
        
        self.attributes.extend( 
            [
                Attr( 'Attenuation', pm.Vec3, SL.getAttenuation, SL.setAttenuation ),
                Attr( 'Exponent', float, SL.getExponent, SL.setExponent ),
                Attr( 'Specular Color', pm.Vec4, SL.getSpecularColor, SL.setSpecularColor ),
                Attr( 'Shadow Caster', bool, SL.isShadowCaster, SL.setShadowCaster )
            ]
        )