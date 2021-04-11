import panda3d.core as pm
from panda3d.core import Spotlight as SL

from game.nodes.manager import import_wrapper


Attr = import_wrapper('nodes.attributes.NodeAttribute')
LensNode = import_wrapper('nodes.lensNode.LensNode')
Light = import_wrapper('nodes.light.Light')



class Spotlight(Light, LensNode):
    
    type_ = SL
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            Attr('Attenuation', pm.Vec3, SL.getAttenuation, SL.setAttenuation),
            Attr('Exponent', float, SL.getExponent, SL.setExponent),
            Attr('Specular Color', pm.Vec4, SL.getSpecularColor, SL.setSpecularColor),
            Attr('Shadow Caster', bool, SL.isShadowCaster, SL.setShadowCaster),
            parent='Spotlight'
       )
