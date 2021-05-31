import unittest

from pandaEditor.nodes.tests.test_nodepath import (
    TestNodePathMixin,
)
from game.nodes.showbasedefaults import (
    Aspect2d,
    BaseCam,
    BaseCamera,
    Cam2d,
    Camera2d,
    Pixel2d,
    Render,
    Render2d,
)


class TestRender(TestNodePathMixin, unittest.TestCase):

    component = Render

    def test_create(self):
        node = super().test_create()
        self.assertEqual('render', node.name)
        self.assertTrue(node.matrix.is_identity())


class TestBaseCam(TestNodePathMixin, unittest.TestCase):

    component = BaseCam

    def test_create(self):
        node = super().test_create()
        self.assertEqual('cam', node.name)
        self.assertTrue(node.matrix.is_identity())


class TestBaseCamera(TestNodePathMixin, unittest.TestCase):

    component = BaseCamera

    def test_create(self):
        node = super().test_create()
        self.assertEqual('camera', node.name)
        self.assertTrue(node.matrix.is_identity())


class TestRender2d(TestNodePathMixin, unittest.TestCase):

    component = Render2d

    def test_create(self):
        node = super().test_create()
        self.assertEqual('render2d', node.name)
        self.assertTrue(node.matrix.is_identity())


class TestAspect2d(TestNodePathMixin, unittest.TestCase):

    component = Aspect2d

    def test_create(self):
        node = super().test_create()
        self.assertEqual('aspect2d', node.name)
        self.assertFalse(node.matrix.is_identity())


class TestPixel2d(TestNodePathMixin, unittest.TestCase):

    component = Pixel2d

    def test_create(self):
        node = super().test_create()
        self.assertEqual('pixel2d', node.name)
        self.assertFalse(node.matrix.is_identity())


class TestCamera2d(TestNodePathMixin, unittest.TestCase):

    component = Camera2d

    def test_create(self):
        node = super().test_create()
        self.assertEqual('camera2d', node.name)
        self.assertTrue(node.matrix.is_identity())


class TestCam2d(TestNodePathMixin, unittest.TestCase):

    component = Cam2d

    def test_create(self):
        node = super().test_create()
        self.assertEqual('cam2d', node.name)
        self.assertTrue(node.matrix.is_identity())
