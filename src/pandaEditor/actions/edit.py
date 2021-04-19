from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor.actions.base import Base


class Edit(Base):
    
    def __init__(self, obj):
        self.obj = obj
        comp = get_base().node_manager.wrap(self.obj)
        self.modified = comp.modified
    
    def undo(self):
        comp = get_base().node_manager.wrap(self.obj)
        comp.modified = self.modified
    
    def redo(self):
        comp = get_base().node_manager.wrap(self.obj)
        comp.modified = True


class Transform(Edit):
    
    def __init__(self, obj, xform, old_xform):
        super().__init__(obj)
        
        self.xform = xform
        self.old_xform = old_xform
    
    def undo(self):
        self.obj.set_transform(self.old_xform)
        comp = get_base().node_manager.wrap(self.obj)
        comp.modified = self.modified
    
    def redo(self):
        self.obj.set_transform(self.xform)
        comp = get_base().node_manager.wrap(self.obj)
        comp.modified = True
        

class SetAttribute(Edit):
    
    def __init__(self, obj, attr, value):
        super().__init__(obj)
        
        self.attr = attr
        self.value = value
        self.old_value = attr.get()
    
    def undo(self):
        super().undo()
        
        self.attr.set(self.old_value)
    
    def redo(self):
        super().redo()
        
        self.attr.set(self.value)
        

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
        
        self.cnnctn.set(self.oldobjs)
    
    def redo(self):
        super().redo()
        
        self.cnnctn.set(self.tgtobjs)
