import p3d


class Attribute( object ):
    
    def __init__( self, label, pType=None, getFn=None, setFn=None, tgtFn=None, 
                  getArgs=[], setArgs=[], tgtArgs=[], w=True ):
        self.label = label
        self.type = pType
        self.getFn = getFn
        self.setFn = setFn
        self.tgtFn = tgtFn
        self.getArgs = getArgs
        self.setArgs = setArgs
        self.tgtArgs = tgtArgs
        self.w = w
        
        self.children = []
        name = self.label.replace( ' ', '' )
        self.name = name[0].lower() + name[1:]
        
    def GetTarget( self, np ):
        if self.tgtFn is None:
            tgt = np
        else:
            args = self.tgtArgs[:]
            args.insert( 0, np )
            tgt = self.tgtFn( *args )
            
        return tgt
        
    def Get( self, np ):
        args = self.getArgs[:]
        args.insert( 0, self.GetTarget( np ) )
        return self.getFn( *args )
    
    def Set( self, np, val ):
        args = self.setArgs[:]
        args.insert( 0, self.GetTarget( np ) )
        args.append( val )
        return self.setFn( *args )
    

class NodeAttribute( Attribute ):
        
    def GetTarget( self, np ):
        return np.node()
    

class NodePathAttribute( Attribute ):
        
    def GetTarget( self, np ):
        return np
    

class NodePathObjectAttribute( Attribute ):
    
    def __init__( self, label, pType, name ):
        Attribute.__init__( self, label, pType, getattr, setattr, None, [name], [name], None )
    
    def GetTarget( self, np ):
        return p3d.NodePathObject.Get( np )
    

class PyTagAttribute( Attribute ):
    
    def __init__( self, *args, **kwargs ):
        self.pyTagName = kwargs.pop( 'pyTagName' )
        Attribute.__init__( self, *args, **kwargs )
    
    def GetTarget( self, np ):
        return np.getPythonTag( self.pyTagName )