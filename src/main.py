from panda3d.core import ConfigVariableBool, loadPrcFileData
from editor.showbase import ShowBase


editor_mode = ConfigVariableBool('editor_mode', False)
editor_mode.set_value(True)
loadPrcFileData('startup', 'window-type none')
ShowBase().run()
