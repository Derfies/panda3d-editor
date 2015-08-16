from panda3d.core import loadPrcFileData
loadPrcFileData( 'startup', 'window-type none' )

import pandaEditor


app = pandaEditor.App( redirect=False )
app.sb.run()