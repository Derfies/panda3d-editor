from game.nodes.connections import Connection as GameConnection
from game.nodes.connections import NodePathTargetConnection as GameNodePathTargetConnection
from game.nodes.connections import ConnectionList as GameConnectionList
from game.nodes.connections import NodePathSourceConnectionList as GameNodePathSourceConnectionList
from game.nodes.connections import NodePathTargetConnectionList as GameNodePathTargetConnectionList


class Connection( GameConnection ):
    
    def Set( self, tgtComp ):
        
        # Remove any connections
        if tgtComp is None:
            ids = [id for id in base.scene.cnnctns if self.name in base.scene.cnnctns[id]]
            for id in ids:
                toRemove = []
                for tup in base.scene.cnnctns[id][self.name]:
                    if tup[0] == self.srcComp:
                        toRemove.append( tup )
                        
                for rem in toRemove:
                    base.scene.cnnctns[id][self.name].remove( rem )
            
        GameConnection.Set( self, tgtComp )
    
    def Connect( self, tgtComp ):
        GameConnection.Connect( self, tgtComp )
        
        # Get the target's id.
        wrpr = base.game.nodeMgr.Wrap( tgtComp )
        tgtId = wrpr.GetId()
        
        # Remove any connections that may already exist.
        for id in base.scene.cnnctns:
            if self.name in base.scene.cnnctns[id] and id != tgtId:
                base.scene.cnnctns[id][self.name] = []
            
        # Add connections to the scene.
        base.scene.cnnctns.setdefault( tgtId, {} )
        base.scene.cnnctns[tgtId].setdefault( self.name, [] )
        base.scene.cnnctns[tgtId][self.name].append( (self.srcComp, self) )
        

class NodePathTargetConnection( GameNodePathTargetConnection, Connection ): pass
    

class ConnectionList( GameConnectionList ):
    
    def Set( self, tgtComps ):
        
        # Remove any connections for this source component.
        ids = [id for id in base.scene.cnnctns if self.name in base.scene.cnnctns[id]]
        for id in ids:
            toRemove = []
            for tup in base.scene.cnnctns[id][self.name]:
                if tup[0] == self.srcComp:
                    toRemove.append( tup )
                    
            for rem in toRemove:
                base.scene.cnnctns[id][self.name].remove( rem )
                    
        GameConnectionList.Set( self, tgtComps )
    
    def Connect( self, tgtComp ):
        GameConnectionList.Connect( self, tgtComp )
        
        # Add connections to the scene.
        wrpr = base.game.nodeMgr.Wrap( tgtComp )
        id = wrpr.GetId()
        base.scene.cnnctns.setdefault( id, {} )
        base.scene.cnnctns[id].setdefault( self.name, [] )
        
        cnnctnComps = [item[1] for item in base.scene.cnnctns[id][self.name]]
        if self.srcComp not in cnnctnComps:
            base.scene.cnnctns[id][self.name].append( (self.srcComp, self) )
            
        
class NodePathSourceConnectionList( GameNodePathSourceConnectionList, ConnectionList ): pass
class NodePathTargetConnectionList( GameNodePathTargetConnectionList, ConnectionList ): pass