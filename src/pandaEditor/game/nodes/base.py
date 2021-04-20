import copy

from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.attributes import Connection
from game.nodes.componentmetaclass import ComponentMetaClass


class Base(metaclass=ComponentMetaClass):
    
    def __init__(self, data):
        self.data = data

        # Set data for all attributes.
        self.attributes = {}
        for name, attr in self._declared_fields.items():
            copy_attr = copy.deepcopy(attr)
            copy_attr.parent = self
            self.attributes[name] = copy_attr

            # Replace the class attribute with the instantiated one.
            setattr(self, name, copy_attr)

        self._children = []
        self.createArgs = {}
    
    @classmethod
    def create(cls, *args, **kwargs):
        data = kwargs.pop('data', None)
        if data is None:
            try:
                data = cls.type_(**kwargs)
            except TypeError as e:
                print(cls, args, kwargs, e)
                raise
        return cls(data)

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return hash(self) == hash(other)

    @property
    def id(self):
        return get_base().scene.comps.get(self)

    @id.setter
    def id(self, value):
        get_base().scene.comps[self] = value

    @property
    def type(self):
        return type(self).__name__

    @property
    def parent(self):
        return get_base().node_manager.wrap(get_base().scene)

    @parent.setter
    def parent(self, value):
        value.add_child(self)

    @property
    def children(self):
        return self._children
    
    def detach(self):
        get_base().scene.deregister_component(self.data)
    
    def destroy(self):
        pass
    
    def duplicate(self):
        dupe = copy.copy(self.data)
        self.fix_up_duplicate_children(self.data, dupe)
        get_base().scene.register_component(dupe)
        return dupe

    @property
    def connections(self):
        return filter(lambda a: isinstance(a, Connection), self.attributes.values())
    
    def add_child(self, comp):
        raise NotImplementedError
            
    def fix_up_duplicate_children(self, origComp, dupeComp):
        dupeWrpr = get_base().node_manager.wrap(dupeComp)
        dupeWrpr.on_duplicate(origComp, dupeComp)
        
        cDupeWrprs = dupeWrpr.children
        origWrpr = get_base().node_manager.wrap(origComp)
        cOrigWrprs = origWrpr.children
        for i in range(len(cDupeWrprs)):
            self.fix_up_duplicate_children(cOrigWrprs[i].data, cDupeWrprs[i].data)

    def on_duplicate(self, orig, dupe):
        raise NotImplementedError