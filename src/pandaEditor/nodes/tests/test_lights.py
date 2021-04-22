import unittest

from pandaEditor.nodes.tests.test_nodepath import (
    TestNodePathMixin,
)
from game.nodes.lights import (
    Light,
    AmbientLight,
    DirectionalLight,
    PointLight,
    Spotlight
)


class TestLightMixin(TestNodePathMixin):

    component = Light

    def test_create(self):
        comp = super().test_create()
        self.assertEqual('node', comp.name)
        self.assertEqual((1, 1, 1, 1), comp.color_scale)


class TestAmbientLight(TestLightMixin, unittest.TestCase):

    component = AmbientLight


class TestDirectionalLight(TestLightMixin, unittest.TestCase):

    component = DirectionalLight


class TestPointLight(TestLightMixin, unittest.TestCase):

    component = PointLight


class TestSpotlight(TestLightMixin, unittest.TestCase):

    component = Spotlight
