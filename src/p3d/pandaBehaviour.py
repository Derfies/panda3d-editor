from singleTask import SingleTask
from pandaManager import PandaManager as pMgr


class PandaBehaviour( SingleTask ):
    
    cType = 'Script'
    
    def __init__( self, *args, **kwargs ):
        SingleTask.__init__( self, *args, **kwargs )
        
        self.accept( pMgr.PANDA_BEHAVIOUR_INIT, self.Init )
        self.accept( pMgr.PANDA_BEHAVIOUR_START, self.Start )
        self.accept( pMgr.PANDA_BEHAVIOUR_STOP, self.Stop )
        self.accept( pMgr.PANDA_BEHAVIOUR_DEL, self.Del )
        
    def __del__( self ):
        print '  PandaBehaviour: ', self.name, ' DELETED'
        
    def OnInit( self ):
        pass
        
    def Init( self ):
        self.OnInit()
        
    def OnDel( self ):
        pass
        
    def Del( self ):
        self.OnDel()
        