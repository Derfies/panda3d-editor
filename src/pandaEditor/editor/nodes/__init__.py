import sys

from constants import *
import nodePath
sys.modules['game.nodes.nodePath'] = nodePath
import lensNode
sys.modules['game.nodes.lensNode'] = lensNode