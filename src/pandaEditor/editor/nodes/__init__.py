import sys

from constants import *
import connections
sys.modules['game.nodes.connections'] = connections
import base
sys.modules['game.nodes.base'] = base
import sceneRoot
sys.modules['game.nodes.sceneRoot'] = sceneRoot
import nodePath
sys.modules['game.nodes.nodePath'] = nodePath
import modelRoot
sys.modules['game.nodes.modelRoot'] = modelRoot
import actor
sys.modules['game.nodes.actor'] = actor
import lensNode
sys.modules['game.nodes.lensNode'] = lensNode
import light
sys.modules['game.nodes.light'] = light
import bulletWorld
sys.modules['game.nodes.bulletWorld'] = bulletWorld
import bulletRigidBodyNode
sys.modules['game.nodes.bulletRigidBodyNode'] = bulletRigidBodyNode