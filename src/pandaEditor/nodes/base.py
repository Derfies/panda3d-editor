import abc


class Base:

    default_values = {}

    @classmethod
    def get_default_values(cls):
        return cls.default_values.copy()

    @classmethod
    def get_foo(cls):
        return list(cls.get_default_values().keys())

    @property
    @abc.abstractmethod
    def label(self):
        """"""

    def validate_drag_drop(self, dragComp, dropComp):
        return False
    
    def get_attrib(self):
        """
        Return a dictionary with bare minimum data for a component - its type
        and id.
        """

        # TODO: Is this required? Seems like we shouldn't care where the args
        # are stored, and this should be in sceneparser anyway.
        attrib = {
            'id': self.id,
            'type': self.type,
        }
        if attrib['id'] is None:
            del attrib['id']
        return attrib

    @property
    def modified(self):
        return False

    @modified.setter
    def modified(self, value):
        pass

    @property
    def savable(self):
        return True
    
    def is_of_type(self, type_):
        return type_ in self.data.__class__.__mro__
    
    def get_possible_connections(self, comps):
        """
        Return a dict of connections that can be made with the given
        components.

        """
        conns = self.__class__.connections
        for comp in comps:
            conns.update(comp.__class__.connections)
        return conns
    
    def set_default_values(self):
        pass

    @property
    @abc.abstractmethod
    def default_parent(self):
        """"""
    
    def get_sibling_index(self):
        """
        Return the position of of this wrapper's component amongst its sibling
        components.
        """
        parent = self.parent
        return parent.children.index(self) if parent is not None else None

    def on_select(self):
        pass

    def on_deselect(self):
        pass

    def on_drag_drop(self, dragComp, dropComp):
        pass

    @abc.abstractmethod
    def duplicate(self):
        """"""

    def fix_up_duplicate_hierarchy(self, orig, dupe):
        orig_children = orig.children
        dupe_children = dupe.children
        for i in range(len(orig_children)):
            self.fix_up_duplicate_hierarchy(
                orig_children[i],
                dupe_children[i]
            )

    @property
    def connections(self):
        conns = {}
        for name, prop in self.__class__.connections.items():
            targets = getattr(self, name)
            if targets is None:
                continue
            if not prop.many:
                targets = [targets]
            conns[name] = targets
        return conns
