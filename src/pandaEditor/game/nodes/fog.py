import panda3d.core as pm

from .nodePath import NodePath
from .attributes import NodeAttribute as Attr


class Fog( NodePath ):
    
    type_ = pm.Fog
    
    def __init__( self, *args, **kwargs ):
        NodePath.__init__( self, *args, **kwargs )

        self.AddAttributes(
            Attr( 'Color', pm.Vec4, pm.Fog.getColor, pm.Fog.setColor ), 
            Attr( 'Linear Onset Point', pm.Point3, pm.Fog.getLinearOnsetPoint, pm.Fog.setLinearOnsetPoint ), 
            Attr( 'Linear Opaque Point', pm.Point3, pm.Fog.getLinearOpaquePoint, pm.Fog.setLinearOpaquePoint ), 
            Attr( 'Exponential Density', float, pm.Fog.getExpDensity, 
                  pm.Fog.setExpDensity ), 
            parent='Fog'
        )