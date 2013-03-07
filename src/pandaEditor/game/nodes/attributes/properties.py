import p3d
from base import Base


class NodeAttribute( Base ):
        
    def GetSource( self ):
        return self.srcComp.node()
    

class NodePathAttribute( Base ):
        
    def GetSource( self ):
        return self.srcComp
    

class NodePathObjectAttribute( Base ):
    
    def __init__( self, label, pType, name ):
        Base.__init__( self, label, pType, getattr, setattr, None, [name], [name], None )
    
    def GetSource( self ):
        return p3d.NodePathObject.Get( self.srcComp )
    

class PyTagAttribute( Base ):
    
    def __init__( self, *args, **kwargs ):
        self.pyTagName = kwargs.pop( 'pyTagName' )
        Base.__init__( self, *args, **kwargs )
    
    def GetSource( self ):
        return self.srcComp.getPythonTag( self.pyTagName )