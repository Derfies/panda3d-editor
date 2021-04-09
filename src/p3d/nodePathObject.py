class NodePathObject( object ):

    """
    Basic building block class, designed to be attached to a node path in the
    scene graph. Doing this creates a circular reference, so care must be
    taken to clear the python tag on this class' node path before trying to
    remove it.
    """
    
    pyTagName = 'NodePathObject'
    
    def __init__( self, np=None ):
        self.np = None
        
        if np is not None:
            self.Attach( np )
        
    def __del__( self ):
        print(self.pyTagName, ' : ', self.np.getName(), ' DELETED')
        
    def Attach( self, np ):
        self.np = np
        self.np.setPythonTag( self.pyTagName, self )
        
    @classmethod
    def Get( cls, np ):
        return np.getPythonTag( cls.pyTagName )
    
    @classmethod
    def Break( cls, np ):
        np.clearPythonTag( cls.pyTagName )