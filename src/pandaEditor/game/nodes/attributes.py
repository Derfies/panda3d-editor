import p3d
from p3d import commonUtils as cUtils
from game.nodes.wrappermeta import BaseMetaClass
from game.utils import get_lower_camel_case


class Base(metaclass=BaseMetaClass):
    
    def __init__(
        self,
        #label,
        type_=None,
        getFn=None,
        setFn=None,
        srcFn=None,
        getArgs=None,
        setArgs=None,
        srcArgs=None,
        w=True,
        srcComp=None,
        parent=None,
        init_arg=None,
        initName=None,
    ):
        #self.label = ''
        self.type = type_
        self.getFn = getFn
        self.setFn = setFn
        self.srcFn = srcFn
        self.getArgs = getArgs or []
        self.setArgs = setArgs or []
        self.srcArgs = srcArgs or []
        self.w = w
        
        self.srcComp = srcComp
        self.parent = parent
        
        self.init_arg = init_arg
        self.initName = initName
        
        # name = self.label.replace(' ', '')
        # self.name = get_lower_camel_case(name)
        #
        # if initName is None:
        #     initName = self.name
        # self.initName = initName
        #self._init_

    @property
    def label(self):
        return ' '.join(word.title() for word in self.name.split('_'))

    @property
    def init_arg_name(self):
        return self.name
        
    # def GetSource(self):
    #     #print('GET SOURCE:', self.srcComp)
    #     if self.srcFn is None:
    #         src = self.srcComp
    #     else:
    #         args = self.srcArgs[:]
    #         args.insert(0, self.srcComp)
    #         src = self.srcFn(*args)
    #
    #     return src

    @property
    def source(self):
        return self.parent.data
        
    # def Get(self):
    #     args = self.getArgs[:]
    #     args.insert(0, self.GetSource())
    #     return self.getFn(*args)
    #
    # def Set(self, val):
    #     args = self.setArgs[:]
    #     args.insert(0, self.GetSource())
    #     args.append(val)
    #     return self.setFn(*args)

    @property
    def value(self):
        return self.getFn(self.source, *self.srcArgs[:])

    @value.setter
    def value(self, value):
        return self.setFn(self.source, *self.srcArgs[:], value)




class Connection(Base, metaclass=BaseMetaClass):

    def __init__(
        self,
        label,
        type_,
        getFn,
        setFn,
        clearFn,
        srcComp=None,
        args=None
    ):
        Base.__init__(self, label, type_, getFn, setFn, srcComp=srcComp)

        self.clearFn = clearFn
        self.args = args or []

        self.cnnctn = True

    def GetSource(self):
        #print('GET SOURCE:', self.srcComp)
        return self.srcComp

    def GetTarget(self, comp):
        return comp

    def Get(self, arg=None):
        return self.getFn(self.GetSource())

    def Set(self, tgtComp):
        self.clearFn(self.GetSource())
        if tgtComp is not None:
            self.Connect(tgtComp)

    def Connect(self, tgtComp):
        if self.args:
            self.setFn(self.GetSource(), self.GetTarget(tgtComp), *self.args)
        else:
            self.setFn(self.GetSource(), self.GetTarget(tgtComp))

    def Break(self, tgtComp):
        self.clearFn(self.GetSource())


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

    def __init__(
        self,
        label,
        cType,
        getFn,
        setFn,
        clearFn,
        removeFn,
        srcComp=None,
        args=None,
    ):
        self.removeFn = removeFn
        args = args or []
        Connection.__init__(self, label, cType, getFn, setFn, clearFn, srcComp, args)

    def Set(self, tgtComps):
        self.clearFn(self.GetSource())
        if tgtComps is not None:
            for tgtComp in tgtComps:
                self.Connect(tgtComp)

    def Break(self, tgtComp):
        self.removeFn(self.GetSource(), self.GetTarget(tgtComp))


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
        if self.setFn is None:
            return None

        if self.type == dict:
            self.Set(valStr)
        else:
            val = cUtils.UnserializeFromString(valStr, self.type)
            if val is not None:
                self.Set(val)


class Attribute(UnserializeMixin, Base, metaclass=BaseMetaClass):

    pass


class NodeAttribute(UnserializeMixin, Base, metaclass=BaseMetaClass):

    # def GetSource(self):
    #     return self.srcComp.node()
    @property
    def source(self):
        return self.parent.data.node()


class NodePathAttribute(UnserializeMixin, Base, metaclass=BaseMetaClass):

    def GetSource(self):
        return self.srcComp


# class NodePathAttribute2(UnserializeMixin, Base, metaclass=BaseMetaClass):
#
#     def __init__(self, *args, **kwargs):
#         super()


class PyTagAttribute(UnserializeMixin, Base, metaclass=BaseMetaClass):

    def __init__(self, *args, **kwargs):
        self.pyTagName = kwargs.pop('pyTagName')
        super(PyTagAttribute, self).__init__(*args, **kwargs)

    def GetSource(self):
        return self.srcComp.getPythonTag(self.pyTagName)


class NodePathObjectAttribute(PyTagAttribute, metaclass=BaseMetaClass):

    def __init__(self, label, pType, name, pyTagName=None):
        if pyTagName is None:
            pyTagName = p3d.NodePathObject.pyTagName
        args = (label, pType, getattr, setattr, None, [name], [name], None)
        kwargs = {'pyTagName':pyTagName}
        super(NodePathObjectAttribute, self).__init__(*args, **kwargs)
