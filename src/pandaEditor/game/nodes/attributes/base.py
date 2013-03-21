import utils


class Base( object ):
    
    def __init__( self, label, type_=None, getFn=None, setFn=None, srcFn=None, 
                  getArgs=[], setArgs=[], srcArgs=[], w=True, srcComp=None, parent=None ):
        self.label = label
        self.type = type_
        self.getFn = getFn
        self.setFn = setFn
        self.srcFn = srcFn
        self.getArgs = getArgs
        self.setArgs = setArgs
        self.srcArgs = srcArgs
        self.w = w
        
        self.srcComp = srcComp
        self.parent = parent
        
        name = self.label.replace( ' ', '' )
        self.name = utils.GetLowerCamelCase( name )
        
    def GetSource( self ):
        if self.srcFn is None:
            src = self.srcComp
        else:
            args = self.srcArgs[:]
            args.insert( 0, self.srcComp )
            src = self.srcFn( *args )
            
        return src
        
    def Get( self ):
        args = self.getArgs[:]
        args.insert( 0, self.GetSource() )
        return self.getFn( *args )
    
    def Set( self, val ):
        args = self.setArgs[:]
        args.insert( 0, self.GetSource() )
        args.append( val )
        return self.setFn( *args )