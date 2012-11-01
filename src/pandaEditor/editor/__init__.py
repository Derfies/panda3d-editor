import sys
import game
sys.modules['oldGame'] = sys.modules.pop( 'game' )

import nodes
import plugins
from base import Base
