class Base( object ):
    
    def __init__( self, modify=False, modifySelection=False ):
        self.modify = modify
        self.modifySelection = modifySelection
        
    def __call__( self ):
        self.Redo()
    
    def Undo( self ):
        pass
    
    def Redo( self ):
        pass
    
    def Destroy( self ):
        pass