from p3d import commonUtils as cUtils


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



class RegisterMixin:
    
    def Set(self, tgtComp):
        base.scene.ClearConnections(self.srcComp)
        
        super().Set(tgtComp)
    
    def Connect(self, tgtComp):
        print(self.__class__.mro())
        super().Connect(tgtComp)
        
        base.scene.RegisterConnection(tgtComp, self)
        
    def Break(self, tgtComp):
        super().Break(tgtComp)
        
        base.scene.DeregisterConnection(tgtComp, self)


class Base(SerializeMixin):

    pass

#
class Connection(RegisterMixin):

    pass
#
#
# class NodePathTargetConnection(RegisterMixin):
#
#     pass
#
#
# # class ConnectionList(RegisterMixin):
# #
# #     pass
#
#
# class NodePathSourceConnectionList(RegisterMixin):
#
#     pass
#
#
# class NodePathTargetConnectionList(RegisterMixin):
#
#     pass
#
#
# class NodePathSourceConnection(RegisterMixin):
#
#     pass





# class Attribute(SerializeMixin):
#
#     pass
#
#
# class NodeAttribute(SerializeMixin):
#
#     pass
#
#
# class NodePathAttribute(SerializeMixin):
#
#     pass
#
#
# class PyTagAttribute(SerializeMixin):
#
#     pass
#
#
# class NodePathObjectAttribute(SerializeMixin):
#
#     pass