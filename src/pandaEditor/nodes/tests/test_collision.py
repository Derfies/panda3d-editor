import unittest

from pandaEditor.nodes.tests.basecomponenttestcase import (
    TestBaseMixin,
)
from game.nodes.collision import (
    CollisionBox,
    CollisionInvSphere,
    CollisionNode,
    CollisionRay,
    CollisionSphere,
    CollisionCapsule,
)
from pandaEditor.nodes.tests.test_nodepath import (
    TestNodePathMixin,
)


class TestCollisionNode(TestNodePathMixin, unittest.TestCase):

    component = CollisionNode

    def test_create(self):
        node = super().test_create()


class TestCollisionBox(TestBaseMixin, unittest.TestCase):

    component = CollisionBox

    def test_create(self):
        node = super().test_create()


class TestCollisionRay(TestBaseMixin, unittest.TestCase):

    component = CollisionRay

    def test_create(self):
        node = super().test_create()


class TestCollisionSphere(TestBaseMixin, unittest.TestCase):

    component = CollisionSphere

    def test_create(self):
        node = super().test_create()


class TestCollisionInvSphere(TestBaseMixin, unittest.TestCase):

    component = CollisionInvSphere

    def test_create(self):
        node = super().test_create()


class TestCollisionCapsule(TestBaseMixin, unittest.TestCase):

    component = CollisionCapsule

    def test_create(self):
        node = super().test_create()
