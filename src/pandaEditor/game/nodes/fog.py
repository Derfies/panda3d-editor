import panda3d.core as pm

from game.nodes.manager import import_wrapper


Attr = import_wrapper('nodes.attributes.NodeAttribute')
NodePath = import_wrapper('nodes.nodePath.NodePath')


class Fog(NodePath):
    
    type_ = pm.Fog
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attr('Color', pm.Vec4, pm.Fog.getColor, pm.Fog.setColor), 
            Attr('Linear Onset Point', pm.Point3, pm.Fog.getLinearOnsetPoint, pm.Fog.setLinearOnsetPoint), 
            Attr('Linear Opaque Point', pm.Point3, pm.Fog.getLinearOpaquePoint, pm.Fog.setLinearOpaquePoint), 
            Attr('Exponential Density', float, pm.Fog.getExpDensity, 
                  pm.Fog.setExpDensity), 
            parent='Fog'
        )
