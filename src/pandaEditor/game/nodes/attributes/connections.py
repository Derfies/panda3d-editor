from .base import Base


class Connection( Base ):
    
    def __init__( self, label, type_, getFn, setFn, clearFn, srcComp=None, args=[] ):
        Base.__init__( self, label, type_, getFn, setFn, srcComp=srcComp )
        
        self.clearFn = clearFn
        self.args = args
        
        self.cnnctn = True
              
    def GetSource( self ):
        return self.srcComp
        
    def GetTarget( self, comp ):
        return comp
    
    def Get( self, arg=None ):
        return self.getFn( self.GetSource() )
    
    def Set( self, tgtComp ):
        self.clearFn( self.GetSource() )
        if tgtComp is not None:
            self.Connect( tgtComp )
        
    def Connect( self, tgtComp ):
        if self.args:
            self.setFn( self.GetSource(), self.GetTarget( tgtComp ), *self.args )
        else:
            self.setFn( self.GetSource(), self.GetTarget( tgtComp ) )
            
    def Break( self, tgtComp ):
        self.clearFn( self.GetSource() )
        

class NodePathTargetConnection( Connection ):
    
    def GetTarget( self, comp ):
        try:
            return comp.node()
        except AttributeError:
            return comp
        

class ConnectionList( Connection ):
    
    def __init__( self, label, cType, getFn, setFn, clearFn, removeFn, srcComp=None, args=[] ):
        self.removeFn = removeFn
        
        Connection.__init__( self, label, cType, getFn, setFn, clearFn, srcComp, args )
        
    def Set( self, tgtComps ):
        self.clearFn( self.GetSource() )
        if tgtComps is not None:
            for tgtComp in tgtComps:
                self.Connect( tgtComp )

    def Break( self, tgtComp ):
        self.removeFn( self.GetSource(), self.GetTarget( tgtComp ) )
        

class NodePathSourceConnectionList( ConnectionList ):
    
    def GetSource( self ):
        return self.srcComp.node()
        

class NodePathTargetConnectionList( ConnectionList ):
    
    def GetTarget( self, comp ):
        try:
            return comp.node()
        except AttributeError:
            return comp