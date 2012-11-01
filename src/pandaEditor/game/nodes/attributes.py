import p3d
import pandac.PandaModules as pm


class Attribute( object ):
    
    def __init__( self, label, pType=None, GetFn=None, SetFn=None, TgtFn=None, 
                  getArgs=[], setArgs=[], tgtArgs=[], w=True, e=True ):
        self.label = label
        self.type = pType
        self.GetFn = GetFn
        self.SetFn = SetFn
        self.TgtFn = TgtFn
        self.getArgs = getArgs
        self.setArgs = setArgs
        self.tgtArgs = tgtArgs
        self.w = w
        self.e = e
        
        self.children = []
        name = self.label.replace( ' ', '' )
        self.name = name[0].lower() + name[1:]
        
    def GetTarget( self, np ):
        if self.TgtFn is None:
            tgt = np
        else:
            args = self.tgtArgs[:]
            args.insert( 0, np )
            tgt = self.TgtFn( *args )
            
        return tgt
        
    def Get( self, np ):
        args = self.getArgs[:]
        args.insert( 0, self.GetTarget( np ) )
        return self.GetFn( *args )
    
    def Set( self, np, val ):
        args = self.setArgs[:]
        args.insert( 0, self.GetTarget( np ) )
        args.append( val )
        return self.SetFn( *args )
    

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