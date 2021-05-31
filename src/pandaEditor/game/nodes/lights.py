import panda3d.core as pc

from game.nodes.attributes import Attribute
from game.nodes.lensnode import LensNode
from game.nodes.nodepath import NodePath


class Light(NodePath):

    type_ = pc.Light
    color = Attribute(
        pc.Vec4,
        pc.Light.get_color,
        pc.Light.set_color,
        node_data=True,
    )


class AmbientLight(Light):

    type_ = pc.AmbientLight


class DirectionalLight(Light):

    type_ = pc.DirectionalLight
    direction = Attribute(
        pc.Vec3,
        pc.DirectionalLight.get_direction,
        pc.DirectionalLight.set_direction,
        node_data=True,
    )
    point = Attribute(
        pc.Point3,
        pc.DirectionalLight.get_point,
        pc.DirectionalLight.set_point,
        node_data=True,
    )
    specular_colour = Attribute(
        pc.Point3,
        pc.DirectionalLight.get_specular_color,
        pc.DirectionalLight.set_specular_color,
        node_data=True,
    )
    shadow_caster = Attribute(
        bool,
        pc.DirectionalLight.is_shadow_caster,
        pc.DirectionalLight.set_shadow_caster,
        node_data=True,
    )


class PointLight(Light):

    type_ = pc.PointLight
    attenuation = Attribute(
        pc.Vec3,
        pc.PointLight.get_attenuation,
        pc.PointLight.set_attenuation,
        node_data=True,
    )
    point = Attribute(
        pc.Point3,
        pc.PointLight.get_point,
        pc.PointLight.set_point,
        node_data=True,
    )
    specular_color = Attribute(
        pc.Vec4,
        pc.PointLight.get_specular_color,
        pc.PointLight.set_specular_color,
        node_data=True,
    )


class Spotlight(Light, LensNode):

    type_ = pc.Spotlight
    attenuation = Attribute(
        pc.Vec3,
        pc.Spotlight.get_attenuation,
        pc.Spotlight.set_attenuation,
        node_data=True,
    )
    exponent = Attribute(
        float,
        pc.Spotlight.get_exponent,
        pc.Spotlight.set_exponent,
        node_data=True,
    )
    specular_color = Attribute(
        pc.Vec4,
        pc.Spotlight.get_specular_color,
        pc.Spotlight.set_specular_color,
        node_data=True,
    )
    show_caster = Attribute(
        bool,
        pc.Spotlight.is_shadow_caster,
        pc.Spotlight.set_shadow_caster,
        node_data=True,
    )
