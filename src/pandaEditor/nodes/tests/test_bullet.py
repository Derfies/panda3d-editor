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
        debug, world = pc.NodePath(pb.BulletDebugNode()), pb.BulletWorld()
        debug_comp, world_comp = BulletDebugNode(debug), BulletWorld(world)
        world_comp.debug_node = debug_comp
        self.assertEqual(debug.node(), world.get_debug_node())

    def test_append_rigid_body(self):
        rigid, world = pc.NodePath(pb.BulletRigidBodyNode()), pb.BulletWorld()
        rigid_comp, world_comp = BulletRigidBodyNode(rigid), BulletWorld(world)
        world_comp.rigid_bodies.append(rigid_comp)
        self.assertEqual(rigid.node(), world.get_rigid_bodies()[0])

    def test_remove_rigid_body(self):
        rigid, world = pc.NodePath(pb.BulletRigidBodyNode()), pb.BulletWorld()
        world.attach(rigid.node())
        rigid_comp, world_comp = BulletRigidBodyNode(rigid), BulletWorld(world)
        world_comp.rigid_bodies.remove(rigid_comp)
        self.assertEqual(0, len(world.get_rigid_bodies()))
