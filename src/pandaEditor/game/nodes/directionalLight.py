import panda3d.core as pm
from panda3d.core import DirectionalLight as DL

try:
    from pandaEditor.editor.nodes.attributes import NodeAttribute as Attr
    from pandaEditor.editor.nodes.light import Light
except ImportError:
    from pandaEditor.game.nodes.attributes import NodeAttribute as Attr
    from pandaEditor.game.nodes.light import Light


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
