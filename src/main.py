import logging

from panda3d.core import ConfigVariableBool, loadPrcFileData


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)


# Stops the default panda window showing.
loadPrcFileData('startup', 'window-type none')

editor_mode = ConfigVariableBool('editor_mode', False)
editor_mode.set_value(True)
from pandaEditor.showbase import ShowBase
ShowBase().run()
