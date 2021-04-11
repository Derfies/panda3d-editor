from game.nodes.base import Base as GameBase
from game.utils import get_lower_camel_case


class Base(GameBase):
    
    def GetName(self):
        try:
            return self.data.getName()
        except:
            return get_lower_camel_case(type(self.data).__name__)
        
    def ValidateDragDrop(self, dragComp, dropComp):
        return False
    
    def GetAttrib(self):
        """
        Return a dictionary with bare minimum data for a component - its type
        and id.
        """
        attrib = {}
        
        id = self.GetId()
        if id is not None:
            attrib['id'] = id
            
        attrib['type'] = self.GetType()
        
        return attrib
        
    def GetPropertyData(self):
        """
        Return a dictionary of all properties as key / value pairs. Make sure
        that values have been serialised to string.
        """
        propDict = {}
        
        for prop in self.GetAttributes():
            if prop.w and not hasattr(prop, 'cnnctn') :
                propStr = prop.SerializeToString()
                if propStr is not None:
                    propDict[prop.name] = propStr
            
        return propDict
    
    def GetConnectionData(self):
        cnnctnDict = {}
        
        # Put this component's connections into key / value pairs.
        for cnnctn in self.GetAllConnections():
            comps = cnnctn.Get()
            if comps is None:
                continue
            
            ids = []
            try:
                for comp in comps:
                    wrpr = base.game.nodeMgr.Wrap(comp)
                    ids.append(wrpr.GetId())
            except TypeError:
                wrpr = base.game.nodeMgr.Wrap(comps)
                ids.append(wrpr.GetId())
            cnnctnDict[cnnctn.name] = ids
            
        return cnnctnDict
    
    def GetModified(self):
        return False
    
    def SetModified(self, val):
        pass
    
    def OnSelect(self):
        pass
    
    def OnDeselect(self):
        pass
    
    def OnDragDrop(self, dragComp, dropComp):
        pass
    
    def Connect(self, comps, mode):
        if mode in cnnctnMap:
            cnnctn = cnnctnMap[mode](self.data, comps)
            cnnctn.Connect()
    
    def IsOfType(self, cType):
        return cType in type(self.data).mro()
    
    def GetPossibleConnections(self, comps):
        """
        Return a list of connections that can be made with the given 
        components.
        """
        cnnctns = []
        
        for comp in comps:
            wrpr = base.game.nodeMgr.Wrap(comp)
            posCnnctns = [attr for attr in self.GetAttributes() if hasattr(attr, 'cnnctn')]
            posCnnctns.extend(self.cnnctns)
            for cnnctn in posCnnctns:
                if wrpr.IsOfType(cnnctn.type) and cnnctn not in cnnctns:
                    cnnctns.append(cnnctn)
        
        return cnnctns
    
    def SetDefaultValues(self):
        pass
        
    def IsSaveable(self):
        return True
    
    def GetDefaultParent(self):
        return base.scene
    
    @classmethod
    def GetDefaultPropertyData(cls):
        try:
            defPropDict = cls.Create().GetPropertyData()
        except:
            defPropDict = {}
        return defPropDict
    
    def GetSiblingIndex(self):
        """
        Return the position of of this wrapper's component amongst its sibling
        components.
        """
        pWrpr = self.GetParent()
        if pWrpr is None:
            return None
        cComps = [cWrpr.data for cWrpr in pWrpr.GetChildren()]
        return cComps.index(self.data)
