from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor.actions.base import Base


class Select(Base):
    
    def __init__(self, objs):
        self.objs = objs
    
    def undo(self):
        get_base().selection.Remove(self.objs)
    
    def redo(self):
        get_base().selection.Add(self.objs)
