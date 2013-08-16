import p3d
from base import Base
from p3d import commonUtils as cUtils


class UnserializeMixin( object ):
    
    def UnserializeFromString( self, valStr ):
        if self.setFn is None:
            return None
        
        if self.type == dict:
            self.Set( valStr )
        else:
            val = cUtils.UnserializeFromString( valStr, self.type )
            if val is not None:
                self.Set( val )
    

class Attribute( UnserializeMixin, Base ):pass


class NodeAttribute( UnserializeMixin, Base ):
        
    def GetSource( self ):
        return self.srcComp.node()
    

class NodePathAttribute( UnserializeMixin, Base ):
        
    def GetSource( self ):
        return self.srcComp
    

class PyTagAttribute( UnserializeMixin, Base ):
    
    def __init__( self, *args, **kwargs ):
        self.pyTagName = kwargs.pop( 'pyTagName' )
        super( PyTagAttribute, self ).__init__( *args, **kwargs )
    
    def GetSource( self ):
        return self.srcComp.getPythonTag( self.pyTagName )
    

class NodePathObjectAttribute( PyTagAttribute ):
    
    def __init__( self, label, pType, name, pyTagName=None ):
        if pyTagName is None:
            pyTagName = p3d.NodePathObject.pyTagName
        args = (label, pType, getattr, setattr, None, [name], [name], None)
        kwargs = {'pyTagName':pyTagName}
        super( NodePathObjectAttribute, self ).__init__( *args, **kwargs )