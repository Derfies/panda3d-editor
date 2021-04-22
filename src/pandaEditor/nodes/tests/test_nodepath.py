import panda3d.core as pc

from pandaEditor.nodes.tests.basecomponenttestcase import (
    TestBaseMixin,
)
from game.nodes.fog import Fog
from game.nodes.lights import AmbientLight
from game.nodes.nodepath import NodePath
from game.nodes.pandanode import PandaNode


class TestNodePathMixin(TestBaseMixin):

    def test_create(self):
        node = super().test_create()
        self.assertFalse(node.lights)
        self.assertIsNone(node.fog)
        return node

    def test_set_name(self):
        panda = pc.NodePath(pc.PandaNode('panda_node'))
        NodePath(panda).name = 'new name'
        self.assertEqual('new name', panda.get_name())

    def test_set_fog(self):
        np = pc.NodePath('np')
        fog = pc.NodePath(pc.Fog('fog'))
        NodePath(np).fog = Fog(fog)
        self.assertEqual(fog.node(), np.get_fog())

    def test_set_lights(self):
        panda = pc.NodePath(pc.PandaNode('panda_node'))
        light = pc.NodePath(pc.AmbientLight('ambient_light'))
        panda_comp, light_comp = NodePath(panda), AmbientLight(light)
        panda_comp.lights.append(light_comp)
        lights = panda.get_attrib(pc.LightAttrib).get_on_lights()
        self.assertEqual(1, len(lights))
        self.assertEqual(light.node(), lights[0].node())
