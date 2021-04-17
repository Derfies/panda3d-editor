from .base import Base


class Select(Base):
    
    def __init__(self, comps):
        self.comps = comps
    
    def undo(self):
        base.selection.Remove(self.comps)
    
    def redo(self):
        base.selection.Add(self.comps)
