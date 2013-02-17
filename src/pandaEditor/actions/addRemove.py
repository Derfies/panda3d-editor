from base import Base


class AddRemove( Base ):
    
    def __init__( self, comp ):
        self.comp = comp
        self.cnnctns = []
        self.pComp = None
        self.id = None
    
    def _AddComponent( self ):
        
        # Attach the component back to its old parent and set it's id back.
        wrpr = base.game.nodeMgr.Wrap( self.comp )
        wrpr.SetParent( self.pComp )
        if self.id is not None:
            wrpr.SetId( self.id )
        
        # Reconnect the component to other elements in the scene.
        for cnnctn in self.cnnctns:
            cnnctn.Connect( self.comp )
        self.cnnctns = []
        
    def _RemoveComponent( self ):
        
        # Break all connections for the nodes we are trying to remove, then
        # detach them from the scene.
        wrpr = base.game.nodeMgr.Wrap( self.comp )
        id = wrpr.GetId()
        if id in base.scene.cnnctns:
            for tup in base.scene.cnnctns[id].values():
                for items in tup:
                    comp, cnnctn = items
                    cnnctn.Break( self.comp )
                    self.cnnctns.append( cnnctn )
                    
            del base.scene.cnnctns[id]
        
        # Store the parent and id, then detach the component from the scene.
        self.pComp = wrpr.GetParent()
        self.id = wrpr.GetId()
        wrpr.Detach()
    

class Add( AddRemove ):
    
    def Undo( self ):
        AddRemove._RemoveComponent( self )
        
    def Redo( self ): 
        AddRemove._AddComponent( self )
    

class Remove( AddRemove ):
    
    def Undo( self ): 
        AddRemove._AddComponent( self )
        
    def Redo( self ): 
        AddRemove._RemoveComponent( self )