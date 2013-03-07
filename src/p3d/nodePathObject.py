class NodePathObject( object ):

    """
    Basic building block class, designed to be attached to a node path in the
    scene graph. Doing this creates a circular reference, so care must be
    taken to clear the python tag on this class' node path before trying to
    remove it.
    """
    
    tagName = 'NodePathObject'
    
    def __init__( self, np ):
        self.np = np
        self.np.setPythonTag( NodePathObject.tagName, self )
        
    def __del__( self ):
        print NodePathObject.tagName, ' : ', self.np.getName(), ' DELETED'
        
    @classmethod
    def Get( cls, np ):
        return np.getPythonTag( cls.tagName )
    
    @classmethod
    def Break( cls, np ):
        np.clearPythonTag( cls.tagName )