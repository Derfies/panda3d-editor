import panda3d.core as pm

from game.nodes.attributes import NodeAttribute
from game.nodes.nodepath import NodePath


class Fog(NodePath):
    
    type_ = pm.Fog
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            NodeAttribute('Color', pm.Vec4, pm.Fog.getColor, pm.Fog.setColor),
            NodeAttribute('Linear Onset Point', pm.Point3, pm.Fog.getLinearOnsetPoint, pm.Fog.setLinearOnsetPoint),
            NodeAttribute('Linear Opaque Point', pm.Point3, pm.Fog.getLinearOpaquePoint, pm.Fog.setLinearOpaquePoint),
            NodeAttribute('Exponential Density', float, pm.Fog.getExpDensity,
                  pm.Fog.setExpDensity), 
            parent='Fog'
        )
