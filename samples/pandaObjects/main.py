from direct.directbase import DirectStart

import game


# Create game base and load level
game = game.Base()
game.OnInit()
game.Load('scenes/helloWorld.xml')

# Initialise the PandaObject manager and start all scripts.
base.pandaMgr.Init()
base.pandaMgr.Start()
        
run()