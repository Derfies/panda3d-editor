import unittest

import panda3d.bullet as pb
import panda3d.core as pc
from pandaEditor.nodes.tests.basecomponenttestcase import (
    TestBaseMixin,
)
from game.nodes.bullet import (
    BulletBoxShape,
    BulletCapsuleShape,
    BulletCharacterControllerNode,
    BulletDebugNode,
    BulletPlaneShape,
    BulletRigidBodyNode,
    BulletWorld,
)
from pandaEditor.nodes.tests.test_nodepath import (
    TestNodePathMixin,
)


class TestBulletBoxShape(TestBaseMixin, unittest.TestCase):

    component = BulletBoxShape

    def test_create(self):
        node = super().test_create()


class TestBulletCapsuleShape(TestBaseMixin, unittest.TestCase):

    component = BulletCapsuleShape

    def test_create(self):
        node = super().test_create()


class TestBulletCharacterControllerNode(TestBaseMixin, unittest.TestCase):

    component = BulletCharacterControllerNode

    def test_create(self):
        node = super().test_create()


class TestBulletDebugNode(TestNodePathMixin, unittest.TestCase):

    component = BulletDebugNode

    def test_create(self):
        node = super().test_create()


class TestBulletPlaneShape(TestBaseMixin, unittest.TestCase):

    component = BulletPlaneShape

    def test_create(self):
        node = super().test_create()


class TestBulletRigidBodyNode(TestBaseMixin, unittest.TestCase):

    component = BulletRigidBodyNode

    def test_create(self):
        node = super().test_create()


class TestBulletWorld(TestBaseMixin, unittest.TestCase):

    component = BulletWorld

    def test_create(self):
        node = super().test_create()

    def test_set_debug_node(self):
        debug = pb.BulletDebugNode()
        world = pb.BulletWorld()
        BulletWorld(world).debug_node.set(pc.NodePath(debug))
        self.assertEqual(debug, world.get_debug_node())

    def test_set_rigid_body(self):
        rigid_body = pb.BulletRigidBodyNode()
        world = pb.BulletWorld()
        BulletWorld(world).rigid_bodies.connect(pc.NodePath(rigid_body))
        self.assertEqual(rigid_body, world.get_rigid_bodies()[0])