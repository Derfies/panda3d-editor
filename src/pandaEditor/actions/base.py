class Base( object ):
    
    def __call__( self ):
        self.Redo()
    
    def Undo( self ):
        pass
    
    def Redo( self ):
        pass
    
    def Destroy( self ):
        pass