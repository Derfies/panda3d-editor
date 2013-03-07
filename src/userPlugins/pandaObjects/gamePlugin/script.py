import os
import sys
import inspect

from game.nodes.base import Base


class Script( Base ):
    
    @staticmethod
    def GetFileName( filePath ):
        normPath = os.path.normpath( filePath )
        head, tail = os.path.split( normPath )
        return os.path.splitext( tail )[0]
        
    def SetParent( self, pObj ):
        name = self.GetFileName( inspect.getfile( self.data.__class__ ) )
        clsName = name[0].upper() + name[1:]
        pObj.instances[clsName] = self.data
        self.data.np = pObj.np
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        
        # Make sure we're dealing with forward slashes 
        filePath = kwargs.pop( 'filePath' ).replace( '\\', '/' )
        name = cls.GetFileName( filePath )
        
        # If the script path is not absolute then we'll need to search for it.
        # imp.find_module won't take file paths so create a list of search
        # paths by joining the tail of file path to each path in sys.path.
        mod = None
        dirPath = os.path.split( filePath )[0]
        if not os.path.isabs( filePath ):
            for sysPath in sys.path:
                testPath = os.path.join( sysPath, dirPath )
                sys.path.insert( 0, testPath )
                
                try:
                    mod = __import__( name )
                    reload( mod ) # Might need to refresh...
                except:
                    pass
                finally:
                    sys.path.pop( 0 )
                    
                if mod is not None:
                    break
        else:
            sys.path.insert( 0, dirPath )
            mod = __import__( name )
            reload( mod ) # Might need to refresh...
            sys.path.pop( 0 )
        
        if mod is None:
            raise ImportError, ( 'No module named ' + name )
            return None
        
        # Get the class matching the name of the file, attach it to
        # the object
        clsName = name[0].upper() + name[1:]
        class_ = getattr( mod, clsName )
        
        # Save the instance by the class name
        instance = class_( clsName )
        #self.data = instance
        
        return cls( instance )
    
    def SetPropertyData( self, dataDict ):
        
        # Set the instance variables from the supplied dictionary.
        for key, value in dataDict.items():
            setattr( self.data, key, value )