import panda3d.core as pm
from panda3d.core import Spotlight as SL

try:
    from pandaEditor.editor.nodes.attributes import NodeAttribute as Attr
    from pandaEditor.editor.nodes.lensNode import LensNode
    from pandaEditor.editor.nodes.light import Light
except ImportError:
    print('import failed')
    from pandaEditor.game.nodes.attributes import NodeAttribute as Attr
    from pandaEditor.game.nodes.lensNode import LensNode
    from pandaEditor.game.nodes.light import Light


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
