import p3d
from base import Base


class NodeAttribute( Base ):
        
    def GetSource( self ):
        return self.srcComp.node()
    

class NodePathAttribute( Base ):
        
    def GetSource( self ):
        return self.srcComp
    

class PyTagAttribute( Base ):
    
    def __init__( self, *args, **kwargs ):
        self.pyTagName = kwargs.pop( 'pyTagName' )
        Base.__init__( self, *args, **kwargs )
    
    def GetSource( self ):
        return self.srcComp.getPythonTag( self.pyTagName )
    

class NodePathObjectAttribute( PyTagAttribute ):
    
    def __init__( self, label, pType, name, pyTagName=None ):
        if pyTagName is None:
            pyTagName = p3d.NodePathObject.pyTagName
        PyTagAttribute.__init__( self, label, pType, getattr, setattr, None, 
                                 [name], [name], None, pyTagName=pyTagName )