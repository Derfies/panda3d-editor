import os
import time
import threading


class DirectoryWatcher(threading.Thread):
    
    """
    Class for watching a directory and all subdirectories below it for 
    changes.
    """
    
    def __init__(self, root=False):
        super().__init__()
        
        self.root = root
        
        self.daemon = True
        self.running = False
        
    def _recurse( self, dirPath ):
        """
        
        """
        fDict = {}
        
        def setDict( key ):
            fDict[key] = os.path.getmtime( key )
        
        if self.root:
            noval = [
                ([setDict( os.path.join( path, f ) ) for f in files if files], 
                 setDict( path )) 
                for path, dirs, files in os.walk( dirPath, True )
            ]
        else:
            noval = [
                ([setDict( os.path.join( path, f ) ) for f in files if files], 
                 [setDict( os.path.join( path, f ) ) for f in dirs if dirs]) 
                for path, dirs, files in os.walk( dirPath, True )
            ]
            
        return fDict
        
    def setDirectory( self, dirPath ):
        """Set the directory for watching."""
        self.dirPath = dirPath
        self.before = self._recurse( self.dirPath )
    
    def run( self ):
        """
        Main watcher function. Don't use this to start the watcher, use 
        start() to run the daemon instead.
        """
        self.running = True
        while True:
            after = self._recurse( self.dirPath )
            
            # Work out which files were added, removed or modified
            added = [f for f in after if not f in self.before]
            removed = [f for f in self.before if not f in after]
            modified = [
                f for f in after 
                if f in self.before and after[f] != self.before[f]
            ]
            
            # Call handlers
            if added:
                self.onAdded( added )
            if removed:
                self.onRemoved( removed )
            if modified:
                self.onModified( modified )
            
            self.before = after
            
            # Sleep a bit so we don't max out the thread
            time.sleep( 1 )
            
    def onAdded( self, filePaths ):
        pass
    
    def onRemoved( self, filePaths ):
        pass
    
    def onModified( self, filePaths ):
        pass