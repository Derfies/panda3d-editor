import panda3d.core as pc

from game.nodes.attributes import NodeAttribute
from game.nodes.lensnode import LensNode
from game.nodes.nodepath import NodePath


class Light(NodePath):

    type_ = pc.Light
    color = NodeAttribute('', pc.Vec4, pc.Light.get_color, pc.Light.set_color)


class AmbientLight(Light):

    type_ = pc.AmbientLight


class DirectionalLight(Light):

    type_ = pc.DirectionalLight
    direction = NodeAttribute(
        '',
        pc.Vec3,
        pc.DirectionalLight.get_direction,
        pc.DirectionalLight.set_direction,
    )
    point = NodeAttribute(
        '',
        pc.Point3,
        pc.DirectionalLight.get_point,
        pc.DirectionalLight.set_point,
    )
    specular_colour = NodeAttribute(
        '',
        pc.Point3,
        pc.DirectionalLight.get_specular_color,
        pc.DirectionalLight.set_specular_color,
    )
    shadow_caster = NodeAttribute(
        '',
        bool,
        pc.DirectionalLight.is_shadow_caster,
        pc.DirectionalLight.set_shadow_caster,
    )


class PointLight(Light):

    type_ = pc.PointLight

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            NodeAttribute('Attenuation', pc.Vec3, pc.PointLight.getAttenuation, pc.PointLight.setAttenuation),
            NodeAttribute('Point', pc.Point3, pc.PointLight.getPoint, pc.PointLight.setPoint),
            NodeAttribute('Specular Color', pc.Vec4, pc.PointLight.getSpecularColor, pc.PointLight.setSpecularColor),
            parent='PointLight'
        )


class Spotlight(Light, LensNode):

    type_ = pc.Spotlight

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            NodeAttribute('Attenuation', pc.Vec3, pc.Spotlight.getAttenuation, pc.Spotlight.setAttenuation),
            NodeAttribute('Exponent', float, pc.Spotlight.getExponent, pc.Spotlight.setExponent),
            NodeAttribute('Specular Color', pc.Vec4, pc.Spotlight.getSpecularColor, pc.Spotlight.setSpecularColor),
            NodeAttribute('Shadow Caster', bool, pc.Spotlight.isShadowCaster, pc.Spotlight.setShadowCaster),
            parent='Spotlight'
        )
