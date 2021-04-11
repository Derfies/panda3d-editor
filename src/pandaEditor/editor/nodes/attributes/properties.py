from p3d import commonUtils as cUtils
from pandaEditor.game.nodes.attributes import Attribute as GameAttribute
from pandaEditor.game.nodes.attributes import NodeAttribute as GameNodeAttribute
from pandaEditor.game.nodes.attributes import NodePathAttribute as GameNodePathAttribute
from pandaEditor.game.nodes.attributes import PyTagAttribute as GamePyTagAttribute
from pandaEditor.game.nodes.attributes import NodePathObjectAttribute as GameNodePathObjectAttribute


class SerializeMixin:
    
    def SerializeToString(self):
        if self.getFn is None:
            return None
            
        pVal = self.Get()
        if isinstance(pVal, dict):
            propDict = {}
            for name, val in pVal.items():
                propDict[name] = cUtils.SerializeToString(val)
            return propDict
        else:
            return cUtils.SerializeToString(pVal)
        

class Attribute(SerializeMixin, GameAttribute):

    pass


class NodeAttribute(SerializeMixin, GameNodeAttribute):

    pass


class NodePathAttribute(SerializeMixin, GameNodePathAttribute):

    pass


class PyTagAttribute(SerializeMixin, GamePyTagAttribute):

    pass


class NodePathObjectAttribute(SerializeMixin, GameNodePathObjectAttribute):

    pass
