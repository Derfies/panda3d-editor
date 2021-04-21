import collections
from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor.actions.base import Base


class AddRemove(Base):
    
    def __init__(self, comp):
        self.comp = comp
        self.pcomp = None
        self.id = None
        self.connections = []
    
    def _add_component(self):
        
        # Attach the component back to its old parent and set its id back.
        if self.pcomp is not None:
            self.pcomp.add_child(self.comp)
        if self.id is not None:
            self.comp.id = self.id
        
        # Reestablish the connections the component has with the other
        # components in the scene.
        for connection in self.connections:
            comp, cnn_name = connection

            # TODO: Find a better way to figure out if the action is set or
            # append.
            orig_value = getattr(comp, cnn_name)
            if isinstance(orig_value, collections.MutableSequence):
                getattr(comp, cnn_name).append(self.comp)
            else:
                setattr(comp, cnn_name, self.comp)
        self.connections = []
        
    def _remove_component(self):

        # Break all connections for the component we are removing, then store
        # those connections so we can reconnect them if this action is undone.
        for connection in get_base().scene.get_outgoing_connections(self.comp):
            comp, cnn_name = connection

            # TODO: Find a better way to figure out if the action is set or
            # append.
            orig_value = getattr(comp, cnn_name)
            if isinstance(orig_value, collections.MutableSequence):
                getattr(comp, cnn_name).remove(self.comp)
            else:
                setattr(comp, cnn_name, None)
            self.connections.append(connection)
        
        # Store the parent and id, then detach the component from the scene.
        self.pcomp = self.comp.parent
        self.id = self.comp.id
        self.comp.detach()
    

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
