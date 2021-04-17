from direct.showbase.PythonUtil import getBase as get_base

from p3d import commonUtils as cUtils


class Base:

    def SerializeToString(self):
        # if self.getFn is None:
        #     return None

        pVal = self.value
        if isinstance(pVal, dict):
            propDict = {}
            for name, val in pVal.items():
                propDict[name] = cUtils.SerializeToString(val)
            return propDict
        else:
            return cUtils.SerializeToString(pVal)



class Connection:
    
    # def Set(self, tgtComp):
    #     get_base().scene.ClearConnections(self.srcComp)
    #
    #     super().Set(tgtComp)
    
    def connect(self, *args, **kwargs):
        super().connect(*args, **kwargs)

        get_base().scene.register_connection(self)
        
    def break_(self, tgtComp):
        super().break_(tgtComp)
        
        get_base().scene.deregister_connection(tgtComp, self)


# class Base(SerializeMixin):
#
#     pass
#
#
# class Connection(RegisterMixin):
#
#     pass
