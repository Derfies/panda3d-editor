from .base import Base


class Parent( Base ):
    
    def __init__( self, np, parent ):
        self.np = np
        self.parent = parent
        
        self.oldParent = np.getParent()
    
    def Undo( self ):
        self.np.wrtReparentTo( self.oldParent )
    
    def Redo( self ):
        self.np.wrtReparentTo( self.parent )