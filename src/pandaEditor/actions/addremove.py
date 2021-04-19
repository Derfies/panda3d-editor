from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor.actions.base import Base


class AddRemove(Base):
    
    def __init__(self, obj):
        self.obj = obj
        self.pobj = None
        self.id = None
        self.connections = []
    
    def _add_component(self):
        
        # Attach the component back to its old parent and set its id back.
        comp = get_base().node_manager.wrap(self.obj)
        if self.pobj is not None:
            pcomp = get_base().node_manager.wrap(self.pobj)
            pcomp.add_child(comp)
        if self.id is not None:
            comp.id = self.id
        
        # Reestablish the connections the component has with the other
        # components in the scene.
        for connection in self.connections:
            connection.connect(self.obj)
        self.connections = []
        
    def _remove_component(self):

        # Break all connections for the component we are removing, then store
        # those connections so we can reconnect them if this action is undone.
        comp = get_base().node_manager.wrap(self.obj)
        print('SIZE:', get_base().scene.get_outgoing_connections(comp))
        for connection in get_base().scene.get_outgoing_connections(comp):
            print('CLEAR')
            connection.clear(self.obj)
            self.connections.append(connection)
        
        # Store the parent and id, then detach the component from the scene.
        self.pobj = comp.parent.data
        self.id = comp.id
        comp.detach()
    

class Add(AddRemove):
    
    def undo(self):
        super()._remove_component()
        
    def redo(self):
        super()._add_component()
    

class Remove(AddRemove):
    
    def undo(self):
        super()._add_component()
        
    def redo(self):
        super()._remove_component()
