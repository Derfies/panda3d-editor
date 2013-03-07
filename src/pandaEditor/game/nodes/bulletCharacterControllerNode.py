import pandac.PandaModules as pm
from panda3d.bullet import ZUp
from panda3d.bullet import BulletShape as BS
from panda3d.bullet import BulletCapsuleShape as BCS
from panda3d.bullet import BulletCharacterControllerNode as BCCN

from nodePath import NodePath
from attributes import NodeAttribute as Attr
from game.nodes.attributes import NodePathSourceConnectionList as Cnnctn


class BulletCharacterControllerNode( NodePath ):
    
    type_ = BCCN
    initArgs = [BCS(0.4, 1.75 - 2*0.4, ZUp), 0.4, 'bulletCharacterControllerNode']