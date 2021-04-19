import panda3d.core as pc

from pandaEditor.nodes.tests.basecomponenttestcase import (
    TestBaseMixin,
)
from game.nodes.nodepath import NodePath


class TestNodePathMixin(TestBaseMixin):

    def test_create(self):
        node = super().test_create()
        self.assertIsNone(node.lights.get())
        self.assertIsNone(node.fog.get())
        return node

    def test_set_name(self):
        np = pc.NodePath('np')
        NodePath(np).name.set('new name')
        self.assertEqual('new name', np.get_name())

    def test_set_fog(self):
        np = pc.NodePath('np')
        fog = pc.Fog('fog')
        NodePath(np).fog.set(pc.NodePath(fog))
        self.assertEqual(fog, np.get_fog())

    def testt_set_lights(self):
        np = pc.NodePath('np')
        ambient_light = pc.AmbientLight('ambient_light')
        NodePath(np).lights.connect(pc.NodePath(ambient_light))
        lights = np.get_attrib(pc.LightAttrib).get_on_lights()
        self.assertEqual(1, len(lights))
        self.assertEqual(ambient_light, lights[0].node())
