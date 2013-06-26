from p3d import commonUtils as cUtils
from game.nodes.attributes import Attribute as GameAttribute
from game.nodes.attributes import NodeAttribute as GameNodeAttribute
from game.nodes.attributes import NodePathAttribute as GameNodePathAttribute
from game.nodes.attributes import PyTagAttribute as GamePyTagAttribute
from game.nodes.attributes import NodePathObjectAttribute as GameNodePathObjectAttribute


class SerializeMixin( object ):
    
    def SerializeToString( self ):
        pVal = self.Get()
        if type( pVal ) == dict:
            propDict = {}
            for name, val in pVal.items():
                propDict[name] = cUtils.SerializeToString( val )
            return propDict
        else:
            return cUtils.SerializeToString( pVal )
        

class Attribute( SerializeMixin, GameAttribute ): pass
class NodeAttribute( SerializeMixin, GameNodeAttribute ): pass
class NodePathAttribute( SerializeMixin, GameNodePathAttribute ): pass
class PyTagAttribute( SerializeMixin, GamePyTagAttribute ): pass
class NodePathObjectAttribute( SerializeMixin, GameNodePathObjectAttribute ): pass