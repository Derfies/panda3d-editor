import panda3d.core as pm
from panda3d.core import PointLight as PL

from game.nodes.manager import import_wrapper


Attr = import_wrapper('nodes.attributes.NodeAttribute')
Light = import_wrapper('nodes.light.Light')


class PointLight(Light):
    
    type_ = PL
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            Attr('Attenuation', pm.Vec3, PL.getAttenuation, PL.setAttenuation),
            Attr('Point', pm.Point3, PL.getPoint, PL.setPoint),
            Attr('Specular Color', pm.Vec4, PL.getSpecularColor, PL.setSpecularColor),
            parent='PointLight'
       )
