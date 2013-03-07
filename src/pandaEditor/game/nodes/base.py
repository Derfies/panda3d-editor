class Base( object ):
    
    initArgs = None
    
    def __init__( self, data ):
        self.data = data
        
        self.attributes = []
        self.cnnctns = []
        self.children = []
        self.createArgs = {}
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        if cls.initArgs is None:
            comp = cls.type_()
        else:
            comp = cls.type_( *cls.initArgs )
        
        return cls( comp )
    
    def Detach( self ):
        base.scene.DeregisterComponent( self.data )
    
    def Destroy( self ):
        pass
    
    def Duplicate( self, np, dupeNp ):
        pass
    
    def FindProperty( self, name ):
        for attr in self.GetAttributes():
            if attr.name == name:
                return attr
            
    def FindConnection( self, name ):
        for cnnctn in self.GetAllConnections():
            if cnnctn.name == name:
                return cnnctn
    
    def SetParent( self, pComp ):
        if pComp is not None:
            wrpr = base.game.nodeMgr.Wrap( pComp )
            wrpr.AddChild( self.data )
    
    def SetPropertyData( self, propDict ):
        for key, val in propDict.items():
            attr = self.FindProperty( key )
            if attr is not None and attr.setFn is not None:
                attr.Set( self.data, val )
            else:
                print 'Failed to set property: ', key
                
    def SetConnectionData( self, cnctnDict ):
        for key, vals in cnctnDict.items():
            cnnctn = self.FindConnection( key )
            if cnnctn is not None:
                for val in vals:
                    cnnctn.Connect( val )
                
    def GetAttributes( self, addons=False ):
        """
        Return a flat list of all the attributes of this component, including
        all child attributes of attributes.
        """
        attrs = self.attributes[:]
        if addons:
            for wrpr in self.GetAddons():
                for attr in wrpr.GetAttributes( addons ):
                    attrs.append( attr )
                
        return attrs
    
    def GetAllConnections( self ):
        cnnctns = []
        
        for attr in self.GetAttributes():
            if hasattr( attr, 'cnnctn' ):
                cnnctns.append( attr )
                
        return cnnctns
    
    def AddChild( self, comp ):
        pass
    
    def AddAttributes( self, *attrs, **kwargs ):
        parent = kwargs.pop( 'parent', None )
        index = kwargs.pop( 'index', len( self.attributes ) )
        for i in range( len( attrs ) ):
            attrs[i].parent = parent
            attrs[i].srcComp = self.data
            self.attributes.insert( index + i, attrs[i] )