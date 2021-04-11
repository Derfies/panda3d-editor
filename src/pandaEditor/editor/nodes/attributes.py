from game.nodes.attributes import (
    Attribute as GameAttribute,
    NodeAttribute as GameNodeAttribute,
    NodePathAttribute as GameNodePathAttribute,
    NodePathObjectAttribute as GameNodePathObjectAttribute,
    PyTagAttribute as GamePyTagAttribute,
)
from p3d import commonUtils as cUtils
from game.nodes.attributes import Connection as GameConnection
from game.nodes.attributes import NodePathTargetConnection as GameNodePathTargetConnection
from game.nodes.attributes import ConnectionList as GameConnectionList
from game.nodes.attributes import NodePathSourceConnectionList as GameNodePathSourceConnectionList
from game.nodes.attributes import NodePathTargetConnectionList as GameNodePathTargetConnectionList


class RegisterMixin:
    
    def Set(self, tgtComp):
        base.scene.ClearConnections(self.srcComp)
        
        super(RegisterMixin, self).Set(tgtComp)
    
    def Connect(self, tgtComp):
        super(RegisterMixin, self).Connect(tgtComp)
        
        base.scene.RegisterConnection(tgtComp, self)
        
    def Break(self, tgtComp):
        super(RegisterMixin, self).Break(tgtComp)
        
        base.scene.DeregisterConnection(tgtComp, self)


class Connection(RegisterMixin, GameConnection):

    pass


class NodePathTargetConnection(RegisterMixin, GameNodePathTargetConnection):

    pass


class ConnectionList(RegisterMixin, GameConnectionList):

    pass


class NodePathSourceConnectionList(RegisterMixin, GameNodePathSourceConnectionList):

    pass


class NodePathTargetConnectionList(RegisterMixin, GameNodePathTargetConnectionList):

    pass


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