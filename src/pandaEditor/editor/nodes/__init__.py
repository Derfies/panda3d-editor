import sys

from .constants import *
from . import attributes
sys.modules['game.nodes.attributes'] = attributes
from . import base
sys.modules['game.nodes.base'] = base
from . import sceneRoot
sys.modules['game.nodes.sceneRoot'] = sceneRoot
from . import nodePath
sys.modules['game.nodes.nodePath'] = nodePath
from . import showbaseDefault
sys.modules['game.nodes.showbaseDefault'] = showbaseDefault
from . import modelRoot
sys.modules['game.nodes.modelRoot'] = modelRoot
from . import actor
sys.modules['game.nodes.actor'] = actor
from . import lensNode
sys.modules['game.nodes.lensNode'] = lensNode
from . import light
sys.modules['game.nodes.light'] = light
from . import bulletWorld
sys.modules['game.nodes.bulletWorld'] = bulletWorld
from . import bulletRigidBodyNode
sys.modules['game.nodes.bulletRigidBodyNode'] = bulletRigidBodyNode
from . import bulletCharacterControllerNode
sys.modules['game.nodes.bulletCharacterControllerNode'] = bulletCharacterControllerNode