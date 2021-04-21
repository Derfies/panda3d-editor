from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor.actions.base import Base


class Deselect(Base):
    
    def __init__(self, comps):
        self.comps = comps
    
    def undo(self):
        get_base().selection.add(self.comps)
    
    def redo(self):
        get_base().selection.remove(self.comps)
