import copy

from direct.showbase.PythonUtil import getBase as get_base

from p3d import commonUtils as cUtils
from game.nodes.attributes import Connection
from game.utils import get_lower_camel_case
from game.nodes.othermeta import ComponentMetaClass


class Base(metaclass=ComponentMetaClass):
    
    def __init__(self, data):
        self.data = data

        self.attributes = {}

        # Set data for all attributes.
        for name, attr in self._declared_fields.items():
            new_attr = copy.deepcopy(attr)
            self.attributes[name] = new_attr
            new_attr.parent = self

            # Replace the class attribute with the instantiated one.
            setattr(self, name, new_attr)
        
        #self.attributes = []
        # self.cnnctns = []
        self.children = []
        self.createArgs = {}
    
    @classmethod
    def create(cls, *args, **kwargs):
        wrpr = cls(None)
        
        createKwargs = {}
        for attr in wrpr.create_attributes:
            if attr.name in kwargs:

                # Cast
                val = cUtils.UnserializeFromString(kwargs[attr.name], attr.type)
                if val is not None:
                    createKwargs[attr.name] = val
            else:
                createKwargs[attr.init_arg_name] = attr.init_arg
        
        # Default create args to a string of the class name.
        if 'name' in createKwargs and not createKwargs['name']:
            createKwargs['name'] = get_lower_camel_case(cls.type_.__name__)

        print('    ', cls.type_, 'createKwargs:', createKwargs)

        wrpr.data = cls.type_(**createKwargs)
        return wrpr

    @property
    def id(self):
        return get_base().scene.comps.get(self.data)

    @id.setter
    def id(self, value):
        get_base().scene.comps[self.data] = value

    @property
    def type(self):
        return type(self).__name__

    @property
    def parent(self):
        return get_base().node_manager.wrap(get_base().scene)

    @parent.setter
    def parent(self, value):
        #comp = get_base().node_manager.wrap(value)
        value.add_child(self)
    
    def detach(self):
        get_base().scene.deregister_component(self.data)
    
    def destroy(self):
        pass
    
    def duplicate(self):
        dupeComp = copy.copy(self.data)
        get_base().scene.register_component(dupeComp)
        self.fix_up_duplicate_children(self.data, dupeComp)
        return dupeComp
    
    def get_children(self):
        return [] 
    
    def get_add_ons(self):
        return []
    
    def find_property(self, name):
        for attr in self.get_attributes():
            if attr.name == name:
                return attr
            
    # def find_connection(self, name):
    #     return self.attributes[name]
        # for cnnctn in self.get_all_connections():
        #     if cnnctn.name == name:
        #         return cnnctn
    
    def set_property_data(self, propDict):
        """
        Set the wrapper's properties from a dictionary of key / value pairs.
        Values will be strings so we must ask the property to unserialize 
        them first.
        """
        for pName, pValStr in propDict.items():

            prop = self.find_property(pName)
            if prop is not None:
                prop.UnserializeFromString(pValStr)
                
    def set_connection_data(self, cnctnDict):
        for key, vals in cnctnDict.items():
            cnnctn = self.attributes[key]#self.FindConnection(key)
            if cnnctn is not None:
                for val in vals:
                    cnnctn.connect(val)
                
    def get_attributes(self, addons=False):
        """
        Return a flat list of all the attributes of this component, including
        all child attributes of attributes.
        """
        attrs = self.attributes.values()
        if addons:
            for wrpr in self.get_add_ons():
                attrs.extend(wrpr.get_attributes(addons))
                
        return attrs

    @property
    def connections(self):
        return filter(lambda a: isinstance(a, Connection), self.attributes.values())
    
    def add_child(self, comp):
        raise Exception('Cannot parent anything to this')
    
    # def AddAttributes(self, *attrs, **kwargs):
    #     parent = kwargs.pop('parent', None)
    #     index = kwargs.pop('index', len(self.attributes))
    #     for i in range(len(attrs)):
    #         attrs[i].parent = parent
    #         attrs[i].srcComp = self.data
    #         self.attributes.insert(index + i, attrs[i])
            
    def fix_up_duplicate_children(self, origComp, dupeComp):
        dupeWrpr = get_base().node_manager.wrap(dupeComp)
        dupeWrpr.on_duplicate(origComp, dupeComp)
        
        cDupeWrprs = dupeWrpr.get_children()
        origWrpr = get_base().node_manager.wrap(origComp)
        cOrigWrprs = origWrpr.get_children()
        for i in range(len(cDupeWrprs)):
            self.fix_up_duplicate_children(cOrigWrprs[i].data, cDupeWrprs[i].data)
            
    def on_duplicate(self, origComp, dupeComp):
        pass
    
    # def SetData(self, data):
    #     self.data = data
    #     for attr in self.attributes:
    #         attr.srcComp = data

    @property
    def create_attributes(self):
        return filter(lambda a: a.init_arg is not None, self.attributes.values())
