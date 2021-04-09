from .base import Base


class Composite( Base ):
    
    def __init__( self, actions ):
        self.actions = actions
    
    def Undo( self ):
        for actn in reversed( self.actions ):
            actn.Undo()
    
    def Redo( self ):
        for actn in self.actions:
            actn.Redo()
            
    def Destroy( self ):
        for actn in self.actions:
            actn.Destroy()