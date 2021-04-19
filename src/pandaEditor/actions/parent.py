from pandaEditor.actions.base import Base


class Parent(Base):
    
    def __init__(self, np, pnp):
        self.np = np
        self.pnp = pnp
        
        self.old_parent = np.get_parent()
    
    def undo(self):
        self.np.wrt_reparent_to(self.old_parent)
    
    def redo(self):
        self.np.wrt_reparent_to(self.pnp)
