class Base( object ):
    
    def __init__( self, game, name='', sort=0, priority=10 ):
        self.game = game
        self.name = name
        self._sort = sort
        self._priority = priority
        
    def OnInit( self ):
        pass
    
    def RegisterNodeWrapper( self, typeStr, cls ):
        self.game.nodeMgr.nodeWrappers[typeStr] = cls
        
    def RegisterPyTagWrapper( self, typeStr, cls ):
        self.game.nodeMgr.pyTagWrappers[typeStr] = cls
    
    def OnNodeDuplicate( self, np ):
        pass
    
    def OnNodeDestroy( self, np ):
        pass