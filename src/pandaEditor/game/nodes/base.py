import copy

from p3d import commonUtils as cUtils
from game.utils import get_lower_camel_case
from game.nodes.othermeta import ComponentMetaClass


class Base(metaclass=ComponentMetaClass):
    
    def __init__(self, data):
        self.data = data

        self.attributes2 = {}

        # Set data for all attributes.
        for name, attr in self._declared_fields.items():
            new_attr = copy.deepcopy(attr)
            self.attributes2[name] = new_attr
            new_attr.parent = self
            new_attr.data = new_attr.srcComp = self.data

            # Replace the class attribute with the instantiated one.
            setattr(self, name, new_attr)
        
        self.attributes = []
        self.cnnctns = []
        self.children = []
        self.createArgs = {}
    
    @classmethod
    def Create(cls, *args, **kwargs):
        #print(args, kwargs)
        wrpr = cls(None)
        
        createKwargs = {}
        for attr in wrpr.create_attributes:
            print('found create attr:', attr.name, 'in kwargs:', attr.name in kwargs)
            if attr.name in kwargs:

                # Cast
                val = cUtils.UnserializeFromString(kwargs[attr.name], attr.type)
                if val is not None:
                    createKwargs[attr.name] = val
            else:
                print(cls, '->', attr.init_arg_name)
                createKwargs[attr.init_arg_name] = attr.init_arg
        
        # Default create args to a string of the class name.
        if 'name' in createKwargs and not createKwargs['name']:
            createKwargs['name'] = get_lower_camel_case(cls.type_.__name__)

        try:
            wrpr.SetData(cls.type_(**createKwargs))
        except Exception as e:
            print('final:', cls, createKwargs)
            raise
        
        return wrpr
    
    def Detach(self):
        base.scene.DeregisterComponent(self.data)
    
    def Destroy(self):
        pass
    
    def Duplicate(self):
        dupeComp = copy.copy(self.data)
        base.scene.RegisterComponent(dupeComp)
        self.FixUpDuplicateChildren(self.data, dupeComp)
        return dupeComp
    
    def GetId(self):
        if self.data in base.scene.comps:
            return base.scene.comps[self.data]
        
        return None
    
    def SetId(self, id):
        base.scene.comps[self.data] = id
        
    def GetType(self):
        return type(self).__name__
        
    def GetParent(self):
        return base.node_manager.Wrap(base.scene)
    
    def SetParent(self, pComp):
        if pComp is not None:
            wrpr = base.node_manager.Wrap(pComp)
            wrpr.AddChild(self.data)
    
    def GetChildren(self):
        return [] 
    
    def GetAddons(self):
        return []
    
    def FindProperty(self, name):
        for attr in self.GetAttributes():
            if attr.name == name:
                return attr
            
    def FindConnection(self, name):
        for cnnctn in self.GetAllConnections():
            if cnnctn.name == name:
                return cnnctn
    
    def SetPropertyData(self, propDict):
        """
        Set the wrapper's properties from a dictionary of key / value pairs.
        Values will be strings so we must ask the property to unserialize 
        them first.
        """
        for pName, pValStr in propDict.items():
            prop = self.FindProperty(pName)
            if prop is not None:
                prop.UnserializeFromString(pValStr)
                
    def SetConnectionData(self, cnctnDict):
        for key, vals in cnctnDict.items():
            cnnctn = self.FindConnection(key)
            if cnnctn is not None:
                for val in vals:
                    cnnctn.Connect(val)
                
    def GetAttributes(self, addons=False):
        """
        Return a flat list of all the attributes of this component, including
        all child attributes of attributes.
        """
        attrs = self.attributes[:]
        if addons:
            for wrpr in self.GetAddons():
                for attr in wrpr.GetAttributes(addons):
                    attrs.append(attr)
                
        return attrs
    
    def GetAllConnections(self):
        cnnctns = []
        
        for attr in self.GetAttributes():
            if hasattr(attr, 'cnnctn'):
                cnnctns.append(attr)
                
        return cnnctns
    
    def AddChild(self, comp):
        pass
    
    def AddAttributes(self, *attrs, **kwargs):
        parent = kwargs.pop('parent', None)
        index = kwargs.pop('index', len(self.attributes))
        for i in range(len(attrs)):
            attrs[i].parent = parent
            attrs[i].srcComp = self.data
            self.attributes.insert(index + i, attrs[i])
            
    def FixUpDuplicateChildren(self, origComp, dupeComp):
        dupeWrpr = base.node_manager.Wrap(dupeComp)
        dupeWrpr.OnDuplicate(origComp, dupeComp)
        
        cDupeWrprs = dupeWrpr.GetChildren()
        origWrpr = base.node_manager.Wrap(origComp)
        cOrigWrprs = origWrpr.GetChildren()
        for i in range(len(cDupeWrprs)):
            self.FixUpDuplicateChildren(cOrigWrprs[i].data, cDupeWrprs[i].data)
            
    def OnDuplicate(self, origComp, dupeComp):
        pass
    
    def SetData(self, data):
        self.data = data
        for attr in self.attributes:
            attr.srcComp = data

    @property
    def create_attributes(self):
        print('create_attributes:', self, self.attributes2)
        for attr in self.attributes2.values():
            print(attr.name, '->', attr.init_arg)
        return filter(lambda a: a.init_arg is not None, self.attributes2.values())
