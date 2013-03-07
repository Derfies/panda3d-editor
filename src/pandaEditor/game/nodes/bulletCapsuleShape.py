import pandac.PandaModules as pm
from panda3d.bullet import BulletCapsuleShape as BCS

from base import Base
from attributes import Attribute as Attr


class BulletCapsuleShape( Base ):
    
    type_ = BCS
    initArgs = [pm.Vec3( 0.5, 0.5, 0.5 )]