import logging
import unittest

from panda3d.core import ConfigVariableBool


ConfigVariableBool('editor_mode', False).set_value(True)
ConfigVariableBool('no_ui', False).set_value(True)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)


if __name__ == '__main__':
    suite = unittest.TestLoader().discover('.', pattern = 'test_*.py')
    unittest.TextTestRunner(verbosity=2).run(suite)
