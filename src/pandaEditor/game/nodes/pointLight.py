import pandac.PandaModules as pm
from pandac.PandaModules import PointLight as PL

from light import Light
from attributes import NodeAttribute as Attr


class PointLight( Light ):
    
    type_ = PL
    
    def __init__( self, *args, **kwargs ):
        Light.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Attenuation', pm.Vec3, PL.getAttenuation, PL.setAttenuation ),
            Attr( 'Point', pm.Point3, PL.getPoint, PL.setPoint ),
            Attr( 'Specular Color', pm.Vec4, PL.getSpecularColor, PL.setSpecularColor ),
            parent='PointLight'
        )