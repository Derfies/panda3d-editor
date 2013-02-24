class Base( object ):
    
    def __init__( self, data=None, cType=None ):
        self.data = data
        self.type = cType
        
        self.attributes = []
        self.cnnctns = []
        self.children = []
        self.createArgs = {}
        self.initArgs = None
            
        # Generate a default name from the node type.
        if self.type is not None:
            nodeName = self.type.__name__
            self.nodeName = nodeName[0:1].lower() + nodeName[1:]
    
    def Create( self, *args, **kwargs ):
        if self.initArgs is None:
            comp = self.type()
        else:
            comp = self.type( *self.initArgs )
        self.data = comp
        
        return comp
    
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
                
    def GetAttributes( self, flat=True, addons=False ):
        """
        Return a flat list of all the attributes of this component, including
        all child attributes of attributes.
        """
        def RecurseGet( cAttr, results ):
            for child in cAttr.children:
                results.append( child )
                RecurseGet( child, results )
        
        attrs = self.attributes[:]
        
        if flat:
            for attr in self.attributes:
                RecurseGet( attr, attrs )
                
        if addons:
            for wrpr in self.GetAddons():
                for attr in wrpr.GetAttributes( flat, addons ):
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