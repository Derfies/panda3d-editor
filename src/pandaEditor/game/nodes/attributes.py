from game.nodes.wrappermeta import BaseMetaClass


class Base(metaclass=BaseMetaClass):
    
    def __init__(
        self,
        type_,
        get_fn=None,
        set_fn=None,
        init_arg=None,
        init_arg_name=None,
        serialise=True,
    ):
        self.type = type_
        self.get_fn = get_fn
        self.set_fn = set_fn
        self.init_arg = init_arg
        self._init_arg_name = init_arg_name
        self._serialise = serialise

    @property
    def label(self):
        return ' '.join(word.title() for word in self.name.split('_'))

    @property
    def init_arg_name(self):
        return self._init_arg_name or self.name

    @property
    def data(self):
        return self.parent.data

    @property
    def serialise(self):
        return self._serialise and self.get_fn is not None

    def get(self):
        return self.get_fn(self.data)

    def set(self, value):
        self.set_fn(self.data, value)


class Attribute(Base, metaclass=BaseMetaClass):

    pass


class NodeAttribute(Attribute, metaclass=BaseMetaClass):

    @property
    def data(self):
        return super().data.node()


class Connection(Base, metaclass=BaseMetaClass):

    def __init__(
        self,
        type_,
        get_fn=None,
        set_fn=None,
        clear_fn=None,
        init_arg=None,
        init_arg_name=None,
        serialise=True,
    ):
        super().__init__(type_, get_fn, set_fn, init_arg, init_arg_name, serialise)

        self.clear_fn = clear_fn

    def _get_target(self, obj):
        return obj

    def connect(self, value):
        self.set_fn(self.data, self._get_target(value))

    def clear(self, value):
        self.clear_fn(self.data, value)


class Connections(Connection):

    def set(self, values):
        self.clear_fn(self.data)
        for value in values:
            self.connect(value)


class NodeConnection(Connection):

    @property
    def data(self):
        return super().data.node()


class NodeConnections(Connections, NodeConnection):

    pass


class ToNodeConnection(Connection):

    def _get_target(self, obj):
        return obj.node()


class NodeToNodeConnection(NodeConnection, ToNodeConnection):

    pass
