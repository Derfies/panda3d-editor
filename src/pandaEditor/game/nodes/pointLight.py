import panda3d.core as pm
from panda3d.core import PointLight as PL

try:
    from pandaEditor.editor.nodes.light import Light
except ImportError:
    print('import failed')
    from pandaEditor.game.nodes.light import Light
from .attributes import NodeAttribute as Attr


class PointLight(Light):
    
    type_ = PL
    
    def __init__(self, *args, **kwargs):
        Light.__init__(self, *args, **kwargs)
        
        self.AddAttributes(
            Attr('Attenuation', pm.Vec3, PL.getAttenuation, PL.setAttenuation),
            Attr('Point', pm.Point3, PL.getPoint, PL.setPoint),
            Attr('Specular Color', pm.Vec4, PL.getSpecularColor, PL.setSpecularColor),
            parent='PointLight'
        )