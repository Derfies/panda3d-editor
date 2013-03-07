import pandac.PandaModules as pm
from panda3d.bullet import BulletPlaneShape as BPS

from base import Base
from attributes import Attribute as Attr


class BulletPlaneShape( Base ):
    
    type_ = BPS
    initArgs = [pm.Vec3( 0, 0, 1 ), 0]