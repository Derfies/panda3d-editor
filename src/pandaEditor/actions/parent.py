from .base import Base


class Parent(Base):
    
    def __init__(self, np, parent):
        self.np = np
        self.parent = parent
        
        self.oldParent = np.getParent()
    
    def undo(self):
        self.np.wrtReparentTo(self.oldParent)
    
    def redo(self):
        self.np.wrtReparentTo(self.parent)
