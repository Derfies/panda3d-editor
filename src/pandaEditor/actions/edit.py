from .base import Base


class Edit(Base):
    
    def __init__(self, comp):
        self.comp = comp
        wrpr = base.game.node_manager.Wrap(self.comp)
        self.mod = wrpr.GetModified()
    
    def Undo(self):
        wrpr = base.game.node_manager.Wrap(self.comp)
        wrpr.SetModified(self.mod)
    
    def Redo(self):
        wrpr = base.game.node_manager.Wrap(self.comp)
        wrpr.SetModified(True)
        

class Transform(Edit):
    
    def __init__(self, comp, xform, oldXform):
        Edit.__init__(self, comp)
        
        self.xform = xform
        self.oldXform = oldXform
    
    def Undo(self):
        self.comp.setTransform(self.oldXform)
        wrpr = base.game.node_manager.Wrap(self.comp)
        wrpr.SetModified(self.mod)
    
    def Redo(self):
        self.comp.setTransform(self.xform)
        wrpr = base.game.node_manager.Wrap(self.comp)
        wrpr.SetModified(True)
        

class SetAttribute(Edit):
    
    def __init__(self, comp, attr, val):
        Edit.__init__(self, comp)
        
        self.attr = attr
        self.val = val
        
        # Save old values. I've had to cast the value back into its own type
        # so as to get a copy - undo doesn't seem to work otherwise.
        self.oldVal = attr.type(attr.Get())
    
    def Undo(self):
        Edit.Undo(self)
        
        self.attr.Set(self.oldVal)
    
    def Redo(self):
        Edit.Redo(self)
        
        self.attr.Set(self.val)
        

class Connect(Edit):
    
    def __init__(self, tgtComps, cnnctn, fn):
        Edit.__init__(self, cnnctn.srcComp)
        
        self.tgtComps = tgtComps
        self.cnnctn = cnnctn
        self.fn = fn
        
        # Save old values
        self.oldComps = self.cnnctn.Get()
    
    def Undo(self):
        Edit.Undo(self)
        
        self.cnnctn.Set(self.oldComps)
    
    def Redo(self):
        Edit.Redo(self)
        
        for tgtComp in self.tgtComps:
            self.fn(tgtComp)
            

class SetConnections(Edit):
    
    def __init__(self, tgtComps, cnnctn):
        Edit.__init__(self, cnnctn.srcComp)
        
        self.tgtComps = tgtComps
        self.cnnctn = cnnctn
        
        # Save old values
        self.oldComps = self.cnnctn.Get()
    
    def Undo(self):
        Edit.Undo(self)
        
        self.cnnctn.Set(self.oldComps)
    
    def Redo(self):
        Edit.Redo(self)
        
        self.cnnctn.Set(self.tgtComps)
