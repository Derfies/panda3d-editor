import panda3d.core as pc

from game.nodes.attributes import NodeAttribute
from game.nodes.lensnode import LensNode
from game.nodes.nodepath import NodePath


class Light(NodePath):

    type_ = pc.Light
    color = NodeAttribute(pc.Vec4, pc.Light.get_color, pc.Light.set_color)


class AmbientLight(Light):

    type_ = pc.AmbientLight


class DirectionalLight(Light):

    type_ = pc.DirectionalLight
    direction = NodeAttribute(
        pc.Vec3,
        pc.DirectionalLight.get_direction,
        pc.DirectionalLight.set_direction,
    )
    point = NodeAttribute(
        pc.Point3,
        pc.DirectionalLight.get_point,
        pc.DirectionalLight.set_point,
    )
    specular_colour = NodeAttribute(
        pc.Point3,
        pc.DirectionalLight.get_specular_color,
        pc.DirectionalLight.set_specular_color,
    )
    shadow_caster = NodeAttribute(
        bool,
        pc.DirectionalLight.is_shadow_caster,
        pc.DirectionalLight.set_shadow_caster,
    )


class PointLight(Light):

    type_ = pc.PointLight
    attenuation = NodeAttribute(
        pc.Vec3,
        pc.PointLight.get_attenuation,
        pc.PointLight.set_attenuation,
    )
    point = NodeAttribute(
        pc.Point3,
        pc.PointLight.get_point,
        pc.PointLight.set_point,
    )
    specular_color = NodeAttribute(
        pc.Vec4,
        pc.PointLight.get_specular_color,
        pc.PointLight.set_specular_color,
    )


class Spotlight(Light, LensNode):

    type_ = pc.Spotlight
    attenuation = NodeAttribute(
        pc.Vec3,
        pc.Spotlight.get_attenuation,
        pc.Spotlight.set_attenuation,
    )
    exponent = NodeAttribute(
        float,
        pc.Spotlight.get_exponent,
        pc.Spotlight.set_exponent
    )
    specular_color = NodeAttribute(
        pc.Vec4,
        pc.Spotlight.get_specular_color,
        pc.Spotlight.set_specular_color,
    )
    show_caster = NodeAttribute(
        bool,
        pc.Spotlight.is_shadow_caster,
        pc.Spotlight.set_shadow_caster,
    )
