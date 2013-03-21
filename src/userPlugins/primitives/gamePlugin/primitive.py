import copy

import p3d

from constants import *
from game.nodes.nodePath import NodePath


class PrimitiveNPO( p3d.NodePathObject ):
    
    pyTagName = TAG_PRIMITIVE_OBJECT
    
    @staticmethod
    def attrgetter( attr ):
        def get_any( self ):
            return getattr( self, attr )
        return get_any
    
    @staticmethod
    def attrsetter( attr ):
        def set_any( self, value ):
            setattr( self, attr, value )
            self.Rebuild()
        return set_any
    
    def Rebuild( self ):
        pass
    

class Primitive( NodePath ):
    
    def Destroy( self ):
        PrimitiveNPO.Break( self.data )
        NodePath.Destroy( self )
        
    def Duplicate( self ):
        dupeNp = NodePath.Duplicate( self )
        
        # Duplicate the primtive NodePathObject to the duplicated NodePath.
        pyObj = PrimitiveNPO.Get( self.data )
        dupePyObj = copy.copy( pyObj )
        dupePyObj.np = dupeNp
        dupeNp.setPythonTag( PrimitiveNPO.pyTagName, dupePyObj )
        return dupeNp