import sys
import game
sys.modules['oldGame'] = sys.modules.pop('game')

from . import nodes
from . import plugins
from .base import Base
from .scene import Scene
