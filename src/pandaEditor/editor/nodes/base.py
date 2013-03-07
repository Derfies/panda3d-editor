from game.nodes.base import Base as GameBase


class Base( GameBase ):
        
    def ValidateDragDrop( self, dragComp, dropComp ):
        return False
    
    def GetId( self ):
        if self.data in base.scene.comps:
            return base.scene.comps[self.data]
        
        return None
    
    def SetId( self, id ):
        base.scene.comps[self.data] = id
    
    def GetName( self ):
        try:
            return self.data.getName()
        except:
            return type( self.data ).__name__
    
    def GetParent( self ):
        return base.scene
    
    def GetAddons( self ):
        return []
    
    def GetChildren( self ):
        return [] 
        
    def GetPropertyData( self ):
        propDict = {}
        
        # Put this component's properties into key / value pairs.
        props = self.GetAttributes()
        props = [prop for prop in props if not hasattr( prop, 'cnnctn' )]
        for prop in props:
            if prop.w and prop.getFn is not None:
                propDict[prop.name] = prop.Get( self.data )
            
        return propDict
    
    def GetConnectionData( self ):
        cnnctnDict = {}
        
        # Put this component's connections into key / value pairs.
        for cnnctn in self.GetAllConnections():
            comps = cnnctn.Get()
            if comps is None:
                continue
            
            ids = []
            try:
                for comp in comps:
                    wrpr = base.game.nodeMgr.Wrap( comp )
                    ids.append( wrpr.GetId() )
            except TypeError:
                wrpr = base.game.nodeMgr.Wrap( comps )
                ids.append( wrpr.GetId() )
            cnnctnDict[cnnctn.name] = ids
            
        return cnnctnDict
    
    def GetCreateArgs( self ):
        return {}
    
    def GetModified( self ):
        return False
    
    def SetModified( self, val ):
        pass
    
    def OnSelect( self, comp ):
        pass
    
    def OnDeselect( self, comp ):
        pass
    
    def OnDragDrop( self, dragComp, dropComp ):
        pass
    
    def Connect( self, comps, mode ):
        if mode in cnnctnMap:
            cnnctn = cnnctnMap[mode]( self.data, comps )
            cnnctn.Connect()
    
    def IsOfType( self, cType ):
        return cType in type( self.data ).mro()
    
    def GetPossibleConnections( self, comps ):
        """
        Return a list of connections that can be made with the given 
        components.
        """
        cnnctns = []
        
        for comp in comps:
            wrpr = base.game.nodeMgr.Wrap( comp )
            posCnnctns = [attr for attr in self.GetAttributes() if hasattr( attr, 'cnnctn' )]
            posCnnctns.extend( self.cnnctns )
            for cnnctn in posCnnctns:
                if wrpr.IsOfType( cnnctn.type ) and cnnctn not in cnnctns:
                    cnnctns.append( cnnctn )
        
        return cnnctns
    
    def SetDefaultValues( self ):
        
        # Set default parent.
        base.scene.RegisterComponent( self.data )
        
    def IsSaveable( self ):
        return True