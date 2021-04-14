import panda3d.core as pm
from panda3d.core import Light as PandaLight

from game.nodes.attributes import NodeAttribute
from game.nodes.lensnode import LensNode
from game.nodes.nodepath import NodePath


class Light(NodePath):

    type_ = PandaLight

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            NodeAttribute(
                'Color',
                pm.Vec4,
                PandaLight.getColor,
                PandaLight.setColor
            ),
            parent='Light'
        )


class AmbientLight(Light):

    type_ = pm.AmbientLight


class DirectionalLight(Light):

    type_ = pm.DirectionalLight

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            NodeAttribute('Direction', pm.Vec3, pm.DirectionalLight.getDirection, pm.DirectionalLight.setDirection),
            NodeAttribute('Point', pm.Point3, pm.DirectionalLight.getPoint, pm.DirectionalLight.setPoint),
            NodeAttribute('Specular Color', pm.Vec4, pm.DirectionalLight.getSpecularColor, pm.DirectionalLight.setSpecularColor),
            NodeAttribute('Shadow Caster', bool, pm.DirectionalLight.isShadowCaster, pm.DirectionalLight.setShadowCaster),
            parent='DirectionalLight'
        )


class PointLight(Light):

    type_ = pm.PointLight

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            NodeAttribute('Attenuation', pm.Vec3, pm.PointLight.getAttenuation, pm.PointLight.setAttenuation),
            NodeAttribute('Point', pm.Point3, pm.PointLight.getPoint, pm.PointLight.setPoint),
            NodeAttribute('Specular Color', pm.Vec4, pm.PointLight.getSpecularColor, pm.PointLight.setSpecularColor),
            parent='PointLight'
        )


class Spotlight(Light, LensNode):

    type_ = pm.Spotlight

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            NodeAttribute('Attenuation', pm.Vec3, pm.Spotlight.getAttenuation, pm.Spotlight.setAttenuation),
            NodeAttribute('Exponent', float, pm.Spotlight.getExponent, pm.Spotlight.setExponent),
            NodeAttribute('Specular Color', pm.Vec4, pm.Spotlight.getSpecularColor, pm.Spotlight.setSpecularColor),
            NodeAttribute('Shadow Caster', bool, pm.Spotlight.isShadowCaster, pm.Spotlight.setShadowCaster),
            parent='Spotlight'
        )
