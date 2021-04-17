import unittest

from panda3d.core import ConfigVariableString, ConfigVariableBool
ConfigVariableBool('editor_mode', False).set_value(True)

from game.nodes.nodepath import NodePath
from game.nodes.pandanode import PandaNode


class Test(unittest.TestCase):

    def setUp(self):
        ConfigVariableString('window-type', 'none').setValue('none')

    def test_panda_node_create(self):
        panda_node = PandaNode.create({'name': 'test'})
        self.assertEqual('test', panda_node.name.value)