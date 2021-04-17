from p3d import commonUtils as cUtils
from game.nodes.wrappermeta import BaseMetaClass


class Base(metaclass=BaseMetaClass):
    
    def __init__(
        self,
        type_,
        get_fn=None,
        set_fn=None,
        init_arg=None,
        serialise=True,
    ):
        self.type = type_
        self.get_fn = get_fn
        self.set_fn = set_fn
        self.serialise = serialise
        self.init_arg = init_arg

    @property
    def label(self):
        return ' '.join(word.title() for word in self.name.split('_'))

    @property
    def init_arg_name(self):
        return self.name

    @property
    def data(self):
        return self.parent.data

    @property
    def value(self):
        return self.get_fn(self.data)

    @value.setter
    def value(self, value):
        return self.set_fn(self.data, value)


class Connection(Base, metaclass=BaseMetaClass):

    def __init__(
        self,
        type_,
        get_fn=None,
        set_fn=None,
        clear_fn=None,
        init_arg=None,
        serialise=True,
    ):
        super().__init__(type_, get_fn, set_fn, init_arg, serialise)

        #self.target = target
        self.clear_fn = clear_fn
    #     self.args = args or []
    #
    #     self.cnnctn = True
    #
    # # def GetSource(self):
    # #     #print('GET SOURCE:', self.srcComp)
    # #     return self.srcComp
    #
    # def GetTarget(self, comp):
    #     return comp
    #
    # def Get(self, arg=None):
    #     return self.getFn(self.GetSource())
    #
    # def Set(self, tgtComp):
    #     self.clearFn(self.GetSource())
    #     if tgtComp is not None:
    #         self.Connect(tgtComp)
    #
    # def connect(self, target):
    #     self.set_fn(self.data, target)
        # if self.args:
        #     self.setFn(self.GetSource(), self.GetTarget(tgtComp), *self.args)
        # else:
        #     self.setFn(self.GetSource(), self.GetTarget(tgtComp))
    #
    # def Break(self, tgtComp):
    #     self.clearFn(self.GetSource())


class NodeConnection(Connection):
    @property
    def value(self):
        return self.get_fn(self.data)

    @value.setter
    def value(self, value):
        return self.set_fn(self.data, value.node())

    # def connect(self, target):
    #     self.set_fn(self.data, target.node())
    # @property
    # def data(self):
    #     return self.parent.data.node()


class NodePathToNodeConnection(Connection):
    pass


class NodePathSourceConnection(Connection, metaclass=BaseMetaClass):

    def GetSource(self, comp):
        try:
            return comp.node()
        except AttributeError:
            return comp


class NodePathTargetConnection(Connection, metaclass=BaseMetaClass):

    def GetTarget(self, comp):
        try:
            return comp.node()
        except AttributeError:
            return comp


class ConnectionList(Connection):
    pass
    # def __init__(
    #     self,
    #     label,
    #     cType,
    #     getFn,
    #     setFn,
    #     clearFn,
    #     removeFn,
    #     srcComp=None,
    #     args=None,
    # ):
    #     self.removeFn = removeFn
    #     args = args or []
    #     Connection.__init__(self, label, cType, getFn, setFn, clearFn, srcComp, args)
    #
    # def Set(self, tgtComps):
    #     self.clearFn(self.GetSource())
    #     if tgtComps is not None:
    #         for tgtComp in tgtComps:
    #             self.Connect(tgtComp)
    #
    # def Break(self, tgtComp):
    #     self.removeFn(self.GetSource(), self.GetTarget(tgtComp))


class NodePathSourceConnectionList(ConnectionList, metaclass=BaseMetaClass):

    def GetSource(self):
        return self.srcComp.node()


class NodePathTargetConnectionList(ConnectionList, metaclass=BaseMetaClass):

    def GetTarget(self, comp):
        try:
            return comp.node()
        except AttributeError:
            return comp


class UnserializeMixin:

    def UnserializeFromString(self, valStr):

        if self.type == dict:
            self.value = valStr
        else:
            val = cUtils.UnserializeFromString(valStr, self.type)
            if val is not None:
                try:
                    self.value = val
                except Exception as e:
                    print(self.parent, self.name, e)


class Attribute(UnserializeMixin, Base, metaclass=BaseMetaClass):

    pass


class NodeAttribute(UnserializeMixin, Base, metaclass=BaseMetaClass):

    @property
    def data(self):
        return self.parent.data.node()


class PyTagAttribute(UnserializeMixin, Base, metaclass=BaseMetaClass):

    def __init__(self, *args, **kwargs):
        self.pyTagName = kwargs.pop('pyTagName')
        super(PyTagAttribute, self).__init__(*args, **kwargs)

    def GetSource(self):
        return self.srcComp.getPythonTag(self.pyTagName)
