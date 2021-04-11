from panda3d.core import ConfigVariableBool, loadPrcFileData
from pandaEditor.showBase import App


editor_mode = ConfigVariableBool('editor_mode')
editor_mode.set_value(True)
loadPrcFileData('startup', 'window-type none')
App().run()
