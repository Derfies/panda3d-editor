import panda3d.core as pc

from game.nodes.attributes import NodeAttribute
from game.nodes.nodepath import NodePath


class Fog(NodePath):
    
    type_ = pc.Fog
    color = NodeAttribute(pc.Vec4, pc.Fog.get_color, pc.Fog.set_color)
    linear_onset_point = NodeAttribute(
        pc.Point3,
        pc.Fog.get_linear_onset_point,
        pc.Fog.set_linear_onset_point
    )
    linear_opaque_point = NodeAttribute(
        pc.Point3,
        pc.Fog.get_linear_opaque_point,
        pc.Fog.set_linear_opaque_point
    )
    exponential_density = NodeAttribute(
        float,
        pc.Fog.get_exp_density,
        pc.Fog.set_exp_density
    )
