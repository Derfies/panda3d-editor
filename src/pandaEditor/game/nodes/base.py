class Base( object ):
    
    def __init__( self, data=None ):
        self.attributes = []
        self.children = []
        self.createArgs = {}
        
        if data is not None:
            self.Wrap( data )
        
    def Create( self, parent, args ):
        pass
    
    def Duplicate( self, np, dupeNp ):
        pass
    
    def Destroy( self ):
        pass
    
    def GetAttributes( self ):
        return self.attributes[:]
    
    def GetAllAttributes( self ):
        """
        Return a flat list of all the attributes of this component, including
        all child attributes of attributes.
        """
        def RecurseGet( cAttr, results ):
            for child in cAttr.children:
                results.append( child )
                RecurseGet( child, results )
        
        results = []
        for attr in self.attributes:
            results.append( attr )
            RecurseGet( attr, results )
        return results
    
    def FindAttribute( self, name ):
        for attr in self.GetAllAttributes():
            if attr.name == name:
                return attr
    
    def GetData( self ):
        dataDict = {}
        
        # Put this component's attributes into key / value pairs.
        for attr in self.GetAllAttributes():
            if attr.w and attr.GetFn is not None:
                dataDict[attr.name] = attr.Get( self.data )
            
        return dataDict
    
    def SetData( self, dataDict ):
        for key, value in dataDict.items():
            attr = self.FindAttribute( key )
            if attr is not None and attr.SetFn is not None:
                attr.Set( self.data, value )
            else:
                print 'Failed to load attribute: ', key
    
    def Wrap( self, data ):
        self.data = data
    
    def GetChildWrapper( self, name ):
        return None
        