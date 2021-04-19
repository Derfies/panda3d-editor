import unittest

from pandaEditor.nodes.tests.basecomponenttestcase import (
    TestBaseMixin,
    ComponentMixin,
)
from game.nodes.actor import Actor
from game.nodes.base import Base
from game.nodes.bullet import (
    BulletBoxShape,
    BulletCapsuleShape,
    BulletCharacterControllerNode,
    BulletDebugNode,
    BulletPlaneShape,
    BulletRigidBodyNode,
    BulletWorld,
)
from game.nodes.camera import Camera
from game.nodes.collision import (
    CollisionBox,
    CollisionInvSphere,
    CollisionNode,
    CollisionRay,
    CollisionSphere,
    CollisionCapsule,
)
from game.nodes.constants import TAG_NODE_TYPE
from game.nodes.fog import Fog
from game.nodes.lensnode import LensNode
from game.nodes.lights import (
    AmbientLight,
    DirectionalLight,
    PointLight,
    Spotlight
)
from game.nodes.modelnode import ModelNode
from game.nodes.modelroot import ModelRoot
from game.nodes.nodepath import NodePath
from game.nodes.pandanode import PandaNode
from game.nodes.sceneroot import SceneRoot
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
from pandaEditor.scene import Scene


class TestRender(ComponentMixin, unittest.TestCase):

    component = Render

    def test_create(self):
        node = super().test_create()
        self.assertEqual('render', node.name.get())
        self.assertTrue(node.matrix.get().is_identity())


class TestBaseCam(ComponentMixin, unittest.TestCase):

    component = BaseCam

    def test_create(self):
        node = super().test_create()
        self.assertEqual('cam', node.name.get())
        self.assertTrue(node.matrix.get().is_identity())


class TestBaseCamera(ComponentMixin, unittest.TestCase):

    component = BaseCamera

    def test_create(self):
        node = super().test_create()
        self.assertEqual('camera', node.name.get())
        self.assertTrue(node.matrix.get().is_identity())


class TestRender2d(ComponentMixin, unittest.TestCase):

    component = Render2d

    def test_create(self):
        node = super().test_create()
        self.assertEqual('render2d', node.name.get())
        self.assertTrue(node.matrix.get().is_identity())


class TestAspect2d(ComponentMixin, unittest.TestCase):

    component = Aspect2d

    def test_create(self):
        node = super().test_create()
        self.assertEqual('aspect2d', node.name.get())
        self.assertFalse(node.matrix.get().is_identity())


class TestPixel2d(ComponentMixin, unittest.TestCase):

    component = Pixel2d

    def test_create(self):
        node = super().test_create()
        self.assertEqual('pixel2d', node.name.get())
        self.assertFalse(node.matrix.get().is_identity())


class TestCamera2d(ComponentMixin, unittest.TestCase):

    component = Camera2d

    def test_create(self):
        node = super().test_create()
        self.assertEqual('camera2d', node.name.get())
        self.assertTrue(node.matrix.get().is_identity())


class TestCam2d(ComponentMixin, unittest.TestCase):

    component = Cam2d

    def test_create(self):
        node = super().test_create()
        self.assertEqual('cam2d', node.name.get())
        self.assertTrue(node.matrix.get().is_identity())
#
#
# class TestAmbientLight(BaseMixin, unittest.TestCase):
#
#     component = AmbientLight
#
#     def test_create(self):
#         node = super().test_create()
#         self.assertEqual('test', node.name.get())
#
#

#
#

#
#
# class TestCam2d(BaseMixin, unittest.TestCase):
#
#     component = Cam2d
#
#     def test_create(self):
#         node = super().test_create()
#         self.assertEqual('test', node.name.get())
#
#
# class TestCamera(BaseMixin, unittest.TestCase):
#
#     component = Camera
#
#     def test_create(self):
#         node = super().test_create()
#         self.assertEqual('test', node.name.get())
#
#
# class TestCamera2d(BaseMixin, unittest.TestCase):
#
#     component = Camera2d
#
#     def test_create(self):
#         node = super().test_create()
#         self.assertEqual('test', node.name.get())
#
#
# class TestFog(BaseMixin, unittest.TestCase):
#
#     component = Fog
#
#     def test_create(self):
#         node = super().test_create()
#         self.assertEqual('test', node.name.get())
#
#
# class TestLensNode(BaseMixin, unittest.TestCase):
#
#     component = LensNode
#
#     def test_create(self):
#         node = super().test_create()
#         self.assertEqual('test', node.name.get())
#
#
# class TestModelNode(BaseMixin, unittest.TestCase):
#
#     component = ModelNode
#
#     def test_create(self):
#         node = super().test_create()
#         self.assertEqual('test', node.name.get())
#
#
# class TestModelRoot(BaseMixin, unittest.TestCase):
#
#     component = ModelNode
#
#     def test_create(self):
#         node = super().test_create()
#         self.assertEqual('test', node.name.get())
#
#
# class TestNodePath(BaseMixin, unittest.TestCase):
#
#     component = ModelNode
#
#     def test_create(self):
#         node = super().test_create()
#         self.assertEqual('test', node.name.get())
#
#
# class TestPandaNode(BaseMixin, unittest.TestCase):
#
#     component = ModelNode
#
#     def test_create(self):
#         node = super().test_create()
#         self.assertEqual('test', node.name.get())
#
#
# class TestPixel2d(BaseMixin, unittest.TestCase):
#
#     component = ModelNode
#
#     def test_create(self):
#         node = super().test_create()
#         self.assertEqual('test', node.name.get())
#
#
# class TestPointLight(BaseMixin, unittest.TestCase):
#
#     component = PointLight
#
#     def test_create(self):
#         node = super().test_create()
#         self.assertEqual('test', node.name.get())
#
#
# class TestSceneRoot(BaseMixin, unittest.TestCase):
#
#     component = SceneRoot
#
#     def test_create(self):
#         self.base.scene = Scene()
#         node = super().test_create()
#         self.assertEqual('test', node.name.get())
#
#
# class TestSpotlight(BaseMixin, unittest.TestCase):
#
#     component = Spotlight
#
#     def test_create(self):
#         node = super().test_create()
#         self.assertEqual('test', node.name.get())