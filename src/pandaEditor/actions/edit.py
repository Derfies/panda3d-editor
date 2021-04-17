from .base import Base


class Edit(Base):
    
    def __init__(self, comp):
        self.comp = comp
        wrpr = base.node_manager.wrap(self.comp)
        self.mod = wrpr.modified
    
    def undo(self):
        wrpr = base.node_manager.wrap(self.comp)
        wrpr.modified = self.mod
    
    def redo(self):
        wrpr = base.node_manager.wrap(self.comp)
        wrpr.modified = True
        

class Transform(Edit):
    
    def __init__(self, comp, xform, oldXform):
        Edit.__init__(self, comp)
        
        self.xform = xform
        self.oldXform = oldXform
    
    def undo(self):
        self.comp.setTransform(self.oldXform)
        wrpr = base.node_manager.wrap(self.comp)
        wrpr.modified = self.mod
    
    def redo(self):
        self.comp.setTransform(self.xform)
        wrpr = base.node_manager.wrap(self.comp)
        wrpr.modified = True
        

class SetAttribute(Edit):
    
    def __init__(self, comp, attr, val):
        Edit.__init__(self, comp)
        
        self.attr = attr
        self.val = val
        
        # Save old values. I've had to cast the value back into its own type
        # so as to get a copy - undo doesn't seem to work otherwise.
        self.oldVal = attr.value#attr.type(attr.value)
    
    def undo(self):
        Edit.undo(self)
        
        self.attr.Set(self.oldVal)
    
    def redo(self):
        Edit.redo(self)
        
        self.attr.value = self.val
        

class Connect(Edit):
    
    def __init__(self, tgtComps, cnnctn, fn):
        Edit.__init__(self, cnnctn.srcComp)
        
        self.tgtComps = tgtComps
        self.cnnctn = cnnctn
        self.fn = fn
        
        # Save old values
        self.oldComps = self.cnnctn.Get()
    
    def undo(self):
        Edit.undo(self)
        
        self.cnnctn.Set(self.oldComps)
    
    def redo(self):
        Edit.redo(self)
        
        for tgtComp in self.tgtComps:
            self.fn(tgtComp)
            

class SetConnections(Edit):
    
    def __init__(self, tgtComps, cnnctn):
        Edit.__init__(self, cnnctn.srcComp)
        
        self.tgtComps = tgtComps
        self.cnnctn = cnnctn
        
        # Save old values
        self.oldComps = self.cnnctn.Get()
    
    def undo(self):
        Edit.undo(self)
        
        self.cnnctn.Set(self.oldComps)
    
    def redo(self):
        Edit.redo(self)
        
        self.cnnctn.Set(self.tgtComps)
