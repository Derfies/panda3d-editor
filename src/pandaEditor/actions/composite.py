from .base import Base


class Composite(Base):
    
    def __init__(self, actions):
        self.actions = actions
    
    def undo(self):
        for actn in reversed(self.actions):
            actn.undo()
    
    def redo(self):
        for actn in self.actions:
            actn.redo()
            
    def destroy(self):
        for actn in self.actions:
            actn.destroy()
