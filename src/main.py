import logging

from panda3d.core import ConfigVariableBool, loadPrcFileData
from showbase import ShowBase



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)
editor_mode = ConfigVariableBool('editor_mode', False)
editor_mode.set_value(True)
loadPrcFileData('startup', 'window-type none')
ShowBase().run()
