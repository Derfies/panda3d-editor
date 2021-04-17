from .base import Base


class AddRemove(Base):
    
    def __init__(self, comp):
        self.comp = comp
        self.cnnctns = []
        self.pComp = None
        self.id = None
    
    def _AddComponent(self):
        
        # Attach the component back to its old parent and set its id back.
        wrpr = base.node_manager.wrap(self.comp)
        if self.pComp is not None:
            wrpr.parent = self.pComp
        if self.id is not None:
            wrpr.set_id(self.id)
        
        # Reestablish the connections the component has with the other 
        # components in the scene.
        for cnnctn in self.cnnctns:
            cnnctn.connect(self.comp)
        self.cnnctns = []
        
    def _RemoveComponent(self):
        
        # Break all connections for the component we are removing, then store
        # those connections so we can reconnect them if this action is undone.
        wrpr = base.node_manager.wrap(self.comp)
        for cnnctn in base.scene.get_outgoing_connections(wrpr):
            cnnctn.break_(self.comp)
            self.cnnctns.append(cnnctn)
        
        # Store the parent and id, then detach the component from the scene.
        self.pComp = wrpr.parent.data
        self.id = wrpr.id
        wrpr.detach()
    

class Add(AddRemove):
    
    def undo(self):
        AddRemove._RemoveComponent(self)
        
    def redo(self):
        AddRemove._AddComponent(self)
    

class Remove(AddRemove):
    
    def undo(self):
        AddRemove._AddComponent(self)
        
    def redo(self):
        AddRemove._RemoveComponent(self)
