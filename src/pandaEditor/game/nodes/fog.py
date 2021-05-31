import panda3d.core as pc

from game.nodes.attributes import Attribute
from game.nodes.nodepath import NodePath


class Fog(NodePath):
    
    type_ = pc.Fog
    color = Attribute(
        pc.Vec4,
        pc.Fog.get_color,
        pc.Fog.set_color,
        node_data=True
    )
    linear_onset_point = Attribute(
        pc.Point3,
        pc.Fog.get_linear_onset_point,
        pc.Fog.set_linear_onset_point,
        node_data=True,
    )
    linear_opaque_point = Attribute(
        pc.Point3,
        pc.Fog.get_linear_opaque_point,
        pc.Fog.set_linear_opaque_point,
        node_data=True,
    )
    exponential_density = Attribute(
        float,
        pc.Fog.get_exp_density,
        pc.Fog.set_exp_density,
        node_data=True,
    )
