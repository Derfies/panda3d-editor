from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor.actions.base import Base


class Edit(Base):
    
    def __init__(self, comp):
        self.comp = comp
        self.old_modified = comp.modified
    
    def undo(self):
        self.comp.modified = self.old_modified
    
    def redo(self):
        self.comp.modified = True


class Transform(Edit):
    
    def __init__(self, comp, xform, old_xform):
        super().__init__(comp)
        self.xform = xform
        self.old_xform = old_xform
    
    def undo(self):
        super().undo()
        self.comp.data.set_transform(self.old_xform)
    
    def redo(self):
        super().redo()
        self.comp.data.set_transform(self.xform)
        

class SetAttribute(Edit):
    
    def __init__(self, comp, name, value):
        super().__init__(comp)
        self.name = name
        self.value = value
        self.old_value = getattr(comp, name)
    
    def undo(self):
        super().undo()
        setattr(self.comp, self.name, self.old_value)
    
    def redo(self):
        super().redo()
        setattr(self.comp, self.name, self.value)
        

class Connect(Edit):
    
    def __init__(self, tgtobjs, cnnctn, fn):
        super().__init__(cnnctn.srcobj)
        
        self.tgtobjs = tgtobjs
        self.cnnctn = cnnctn
        self.fn = fn
        self.oldobjs = self.cnnctn.get()
    
    def undo(self):
        super().undo()
        
        self.cnnctn.set(self.oldobjs)
    
    def redo(self):
        super().redo()
        
        for tgtobj in self.tgtobjs:
            self.fn(tgtobj)
            

class SetConnections(Edit):
    
    def __init__(self, tgtobjs, cnnctn):
        super().__init__(cnnctn.data)
        
        self.tgtobjs = tgtobjs
        self.cnnctn = cnnctn
        
        # Save old values
        self.oldobjs = self.cnnctn.get()
    
    def undo(self):
        super().undo()
        
        self.cnnctn = self.oldobjs
    
    def redo(self):
        super().redo()
        
        self.cnnctn.set(self.tgtobjs)
