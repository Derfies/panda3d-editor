class WrappedFunction( object ):
    
    def __init__( self, fn=None ):
        self.fns = []
        
        # Add base function
        if fn is not None:
            self.Add( fn )
        
    def __call__( self, *args, **kwargs ):
        return self.fn( *args, **kwargs )
    
    def Add( self, fn ):
        """Add a function."""
        self.fns.append( fn )
        self.Compile()
        
    def Compile( self ):
        """Compile the final function."""
        compiledFn = self.fns[0]
        for i in range( 1, len( self.fns ) ):
            compiledFn = self.Wrap( compiledFn, self.fns[i] )
        self.fn = compiledFn
            
    def Wrap( self, fn, wrapFn ):
        """Return function fn wrapped with wrapFn."""
        def Wrapped( *args ):
            return wrapFn( *fn( *args ) )
        return Wrapped
        