from game.nodes.attributes import Connection as GameConnection
from game.nodes.attributes import NodePathTargetConnection as GameNodePathTargetConnection
from game.nodes.attributes import ConnectionList as GameConnectionList
from game.nodes.attributes import NodePathSourceConnectionList as GameNodePathSourceConnectionList
from game.nodes.attributes import NodePathTargetConnectionList as GameNodePathTargetConnectionList


class Connection( GameConnection ):
    
    def Set( self, tgtComp ):
        base.scene.ClearConnections( self.srcComp )
        
        GameConnection.Set( self, tgtComp )
    
    def Connect( self, tgtComp ):
        GameConnection.Connect( self, tgtComp )
        
        base.scene.RegisterConnection( tgtComp, self )
        
    def Break( self, tgtComp ):
        GameConnection.Break( self, tgtComp )
        
        base.scene.DeregisterConnection( tgtComp, self )
        

class NodePathTargetConnection( GameNodePathTargetConnection, Connection ): pass
class ConnectionList( GameConnectionList, Connection ): pass
class NodePathSourceConnectionList( GameNodePathSourceConnectionList, ConnectionList ): pass
class NodePathTargetConnectionList( GameNodePathTargetConnectionList, ConnectionList ): pass