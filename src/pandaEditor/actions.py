import abc
import collections
import logging

from direct.showbase.PythonUtil import getBase as get_base


logger = logging.getLogger(__name__)


class Base(metaclass=abc.ABCMeta):

    def __call__(self):
        self.redo()

    @abc.abstractmethod
    def undo(self):
        """"""

    @abc.abstractmethod
    def redo(self):
        """"""

    def destroy(self):
        pass


class Edit(Base):

    def __init__(self, comp):
        self.comp = comp
        self.old_modified = comp.modified

    def undo(self):
        self.comp.modified = self.old_modified

    def redo(self):
        self.comp.modified = True


class Composite(Base):

    def __init__(self, actions):
        self.actions = actions

    def undo(self):
        for action in reversed(self.actions):
            action.undo()

    def redo(self):
        for action in self.actions:
            action.redo()

    def destroy(self):
        for action in self.actions:
            action.destroy()


class Select(Base):

    def __init__(self, comps):
        self.comps = comps

    def undo(self):
        get_base().selection.remove(self.comps)

    def redo(self):
        get_base().selection.add(self.comps)


class Deselect(Base):

    def __init__(self, comps):
        self.comps = comps

    def undo(self):
        get_base().selection.add(self.comps)

    def redo(self):
        get_base().selection.remove(self.comps)


class Parent(Base):

    def __init__(self, comp, pcomp):
        self.comp = comp
        self.pcomp = pcomp

        self.old_pcomp = self.comp.parent

    def undo(self):
        self.comp.data.wrt_reparent_to(self.old_pcomp.data)

    def redo(self):
        self.comp.data.wrt_reparent_to(self.pcomp.data)


class AddRemoveBase(Base):

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


class Add(AddRemoveBase):

    def undo(self):
        super()._remove_component()

    def redo(self):
        super()._add_component()


class Remove(AddRemoveBase):

    def undo(self):
        super()._add_component()

    def redo(self):
        super()._remove_component()


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


class SetConnections(Edit):

    def __init__(self, comp, name, value):
        super().__init__(comp)
        self.name = name
        self.value = value
        self.old_value = getattr(comp, name)

    def undo(self):
        super().undo()
        getattr(self.comp, self.name)[:] = self.old_value

    def redo(self):
        super().redo()
        getattr(self.comp, self.name)[:] = self.value


class Manager:

    def __init__(self):
        self.undos = []
        self.redos = []

    def undo(self):
        if not self.undos:
            logger.info('No more undo')
        else:
            action = self.undos.pop()
            self.redos.append(action)
            action.undo()

    def redo(self):
        if not self.redos:
            logger.info('No more redo')
        else:
            action = self.redos.pop()
            self.undos.append(action)
            action.redo()

    def reset_undo(self):
        while self.undos:
            action = self.undos.pop()
            action.destroy()

    def reset_redo(self):
        while self.redos:
            action = self.redos.pop()
            action.destroy()

    def reset(self):
        self.reset_undo()
        self.reset_redo()

    def push(self, action):
        self.undos.append(action)
        self.reset_redo()