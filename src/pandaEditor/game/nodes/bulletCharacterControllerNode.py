from panda3d.bullet import ZUp
from panda3d.bullet import BulletCapsuleShape as BCS
from panda3d.bullet import BulletCharacterControllerNode as BCCN

from .nodePath import NodePath
from .attributes import NodeAttribute as Attr


class BulletCharacterControllerNode( NodePath ):
    
    type_ = BCCN
    
    def __init__( self, *args, **kwargs ):
        NodePath.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Shape', BCS, initDefault=BCS( 0.4, 1.75 - 2*0.4, ZUp ) ),
            Attr( 'step_height', float, initDefault=0.4 ),
            Attr( 'Name', str ),
            parent='BulletCharacterControllerNode'
        )