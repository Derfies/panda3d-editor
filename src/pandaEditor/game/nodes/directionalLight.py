import panda3d.core as pm
from panda3d.core import DirectionalLight as DL

from game.nodes.manager import import_wrapper


Attr = import_wrapper('nodes.attributes.NodeAttribute')
Light = import_wrapper('nodes.light.Light')


class DirectionalLight(Light):
    
    type_ = DL
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            Attr('Direction', pm.Vec3, DL.getDirection, DL.setDirection),
            Attr('Point',pm.Point3, DL.getPoint, DL.setPoint),
            Attr('Specular Color', pm.Vec4, DL.getSpecularColor, DL.setSpecularColor),
            Attr('Shadow Caster', bool, DL.isShadowCaster, DL.setShadowCaster),
            parent='DirectionalLight'
       )
