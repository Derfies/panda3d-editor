from .object import Object
from direct.task import Task


class SingleTask(Object):
    
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.name = name
        self._task = None
        
    def OnUpdate( self, task ):
        """Override this function with code to be executed each frame."""
        pass
        
    def Update( self, task ):
        """
        Run OnUpdate method - return task.cont if there was no return value.
        """
        result = self.OnUpdate( task )
        if result is None:
            return task.cont
        
        return result
    
    def OnStart( self ):
        """
        Override this function with code to be executed when the object is
        started.
        """
        pass
        
    def Start( self, sort=None, priority=None, delayTime=0 ):
        """Start the object's task if it hasn't been already."""
        # Run OnStart method
        self.OnStart()
        
        if self._task not in taskMgr.getAllTasks():
            if not delayTime:
                self._task = taskMgr.add( self.Update, '%sUpdate' % self.name, sort=sort, priority=priority )
            else:
                self._task = taskMgr.doMethodLater( delayTime, self.Update, '%sUpdate' % self.name, sort=sort, priority=priority )
    
    def OnStop( self ):
        """
        Override this function with code to be executed when the object is
        stopped.
        """
        pass
    
    def Stop( self ):
        """Remove the object's task from the task manager."""
        # Run OnStop method
        self.OnStop()
        
        if self._task in taskMgr.getAllTasks():
            taskMgr.remove( self._task )
            self._task = None
            
    def IsRunning( self ):
        """
        Return True if the object's task can be found in the task manager,
        False otherwise.
        """
        return self._task in taskMgr.getAllTasks()
        