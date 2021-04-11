import copy

from p3d import commonUtils as cUtils
from game.utils import get_lower_camel_case


class Base:
    
    def __init__(self, data):
        self.data = data
        
        self.attributes = []
        self.cnnctns = []
        self.children = []
        self.createArgs = {}
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = cls(None)
        
        createKwargs = {}
        for attr in wrpr.GetCreateAttributes():
            if attr.name in kwargs:
                val = cUtils.UnserializeFromString(kwargs[attr.name], attr.type)
                if val is not None:
                    createKwargs[attr.name] = val
            else:
                createKwargs[attr.initName] = attr.initDefault
        
        # Default create args to a string of the class name.
        if 'name' in createKwargs and not createKwargs['name']:
            createKwargs['name'] = get_lower_camel_case(cls.type_.__name__)
        
        wrpr.SetData(cls.type_(**createKwargs))
        
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
        return base.game.nodeMgr.Wrap(base.scene)
    
    def SetParent(self, pComp):
        if pComp is not None:
            wrpr = base.game.nodeMgr.Wrap(pComp)
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
        dupeWrpr = base.game.nodeMgr.Wrap(dupeComp)
        dupeWrpr.OnDuplicate(origComp, dupeComp)
        
        cDupeWrprs = dupeWrpr.GetChildren()
        origWrpr = base.game.nodeMgr.Wrap(origComp)
        cOrigWrprs = origWrpr.GetChildren()
        for i in range(len(cDupeWrprs)):
            self.FixUpDuplicateChildren(cOrigWrprs[i].data, cDupeWrprs[i].data)
            
    def OnDuplicate(self, origComp, dupeComp):
        pass
    
    def SetData(self, data):
        self.data = data
        for attr in self.attributes:
            attr.srcComp = data
            
    def GetCreateAttributes(self):
        attrs = []
        
        for attr in self.GetAttributes():
            if attr.initDefault is not None:
                attrs.append(attr)
                        
        return attrs