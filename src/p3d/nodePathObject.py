TAG_PANDA_OBJECT = 'PandaObject'


class NodePathObject( object ):

    """
    Basic building block class, designed to be attached to a node path in the
    scene graph. Doing this creates a circular reference, so care must be
    taken to clear the python tag on this class' node path before trying to
    remove it.
    """
    
    def __init__( self, np ):
        self.np = np
        self.np.setPythonTag( TAG_PANDA_OBJECT, self )
        
    def __del__( self ):
        print TAG_PANDA_OBJECT, ' : ', self.np.getName(), ' DELETED'
        
    @staticmethod
    def Get( np ):
        return np.getPythonTag( TAG_PANDA_OBJECT )
    
    @staticmethod
    def Break( np ):
        np.clearPythonTag( TAG_PANDA_OBJECT )