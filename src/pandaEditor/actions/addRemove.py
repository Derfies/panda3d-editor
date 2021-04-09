from .base import Base


class AddRemove( Base ):
    
    def __init__( self, comp ):
        self.comp = comp
        self.cnnctns = []
        self.pComp = None
        self.id = None
    
    def _AddComponent( self ):
        
        # Attach the component back to its old parent and set its id back.
        wrpr = base.game.nodeMgr.Wrap( self.comp )
        wrpr.SetParent( self.pComp )
        if self.id is not None:
            wrpr.SetId( self.id )
        
        # Reestablish the connections the component has with the other 
        # components in the scene.
        for cnnctn in self.cnnctns:
            cnnctn.Connect( self.comp )
        self.cnnctns = []
        
    def _RemoveComponent( self ):
        
        # Break all connections for the component we are removing, then store
        # those connections so we can reconnect them if this action is undone.
        wrpr = base.game.nodeMgr.Wrap( self.comp )
        for cnnctn in base.scene.GetOutgoingConnections( wrpr ):
            cnnctn.Break( self.comp )
            self.cnnctns.append( cnnctn )
        
        # Store the parent and id, then detach the component from the scene.
        self.pComp = wrpr.GetParent().data
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