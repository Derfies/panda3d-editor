from direct.directbase import DirectStart

import game


# Create game base and load level
game = game.Base()
game.OnInit()
game.Load( render, 'maps/test.xml' )
run()