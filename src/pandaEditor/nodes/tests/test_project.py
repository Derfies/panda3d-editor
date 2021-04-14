import logging
import unittest

from panda3d.core import ConfigVariableString


logger = logging.getLogger(__name__)


class Test(unittest.TestCase):

    def test_(self):
        ConfigVariableString('window-type', 'none').setValue('none')
