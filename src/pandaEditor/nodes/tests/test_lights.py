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
    Light,
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


class TestLightMixin(ComponentMixin):

    component = Light
    create_kwargs = {'name': 'test'}

    def test_create(self):
        node = super().test_create()
        self.assertEqual('test', node.name.get())
        self.assertEqual((1, 1, 1, 1), node.color.get())
        return node


class TestAmbientLight(TestLightMixin, unittest.TestCase):

    component = AmbientLight

    def test_create(self):
        node = super().test_create()


class TestDirectionalLight(TestLightMixin, unittest.TestCase):

    component = AmbientLight

    def test_create(self):
        node = super().test_create()


class TestPointLight(TestLightMixin, unittest.TestCase):

    component = PointLight

    def test_create(self):
        node = super().test_create()


class TestSpotlight(TestLightMixin, unittest.TestCase):

    component = Spotlight

    def test_create(self):
        node = super().test_create()
