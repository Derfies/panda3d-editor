import pandac.PandaModules as pm
from pandac.PandaModules import PointLight as PL

from light import Light
from attributes import NodeAttribute as Attr


class PointLight( Light ):
    
    def __init__( self, *args, **kwargs ):
        kwargs['nType'] = PL
        Light.__init__( self, *args, **kwargs )
        
        pAttr = Attr( 'PointLight' )
        pAttr.children.extend( 
            [
                Attr( 'Attenuation', pm.Vec3, PL.getAttenuation, PL.setAttenuation ),
                Attr( 'Point', pm.Point3, PL.getPoint, PL.setPoint ),
                Attr( 'Specular Color', pm.Vec4, PL.getSpecularColor, PL.setSpecularColor )
            ]
        )
        self.attributes.append( pAttr )