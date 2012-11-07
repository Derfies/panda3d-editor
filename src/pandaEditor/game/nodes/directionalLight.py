import pandac.PandaModules as pm
from pandac.PandaModules import DirectionalLight as DL

from light import Light
from attributes import NodeAttribute as Attr


class DirectionalLight( Light ):
    
    def __init__( self, *args, **kwargs ):
        kwargs['nType'] = DL
        Light.__init__( self, *args, **kwargs )
        
        pAttr = Attr( 'DirectionalLight' )
        pAttr.children.extend( 
            [
                Attr( 'Direction', pm.Vec3, DL.getDirection, DL.setDirection ),
                Attr( 'Point',pm.Point3, DL.getPoint, DL.setPoint ),
                Attr( 'Specular Color', pm.Vec4, DL.getSpecularColor, DL.setSpecularColor ),
                Attr( 'Shadow Caster', bool, DL.isShadowCaster, DL.setShadowCaster )
            ]
        )
        self.attributes.append( pAttr )