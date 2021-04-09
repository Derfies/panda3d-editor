import sys

from . import base
sys.modules['game.plugins.base'] = base

from .manager import Manager