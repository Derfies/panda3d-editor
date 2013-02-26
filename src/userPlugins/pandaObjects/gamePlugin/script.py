import os
import sys
import inspect

import pandac.PandaModules as pm

from game.nodes.base import Base


class Script( Base ):
    
    def GetFileName( self, filePath ):
        normPath = os.path.normpath( filePath )
        head, tail = os.path.split( normPath )
        return os.path.splitext( tail )[0]
        
    def SetParent( self, pObj ):
        name = self.GetFileName( inspect.getfile( self.data.__class__ ) )
        clsName = name[0].upper() + name[1:]
        pObj.instances[clsName] = self.data
        self.data.np = pObj.np
        
    def Create( self, *args, **kwargs ):
        
        # Make sure we're dealing with forward slashes 
        filePath = kwargs.pop( 'filePath' ).replace( '\\', '/' )
        name = self.GetFileName( filePath )
        
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
        cls = getattr( mod, clsName )
        
        # Save the instance by the class name
        instance = cls( clsName )
        self.data = instance
        
        return instance
        
    def GetPropertyData( self ):
        
        # Put all instance variables into a dictionary and return it.
        dataDict = {}
        for pName, pType in self.GetProps().items():
            dataDict[pName] = getattr( self.data, pName )
        return dataDict
    
    def SetPropertyData( self, dataDict ):
        
        # Set the instance variables from the supplied dictionary.
        for key, value in dataDict.items():
            setattr( self.data, key, value )
    
    def GetProps( self ):
        props = {}
        for pName, prop in vars( self.data.__class__ ).items():
            if type( prop ) == type:
                props[pName] = prop
                
        return props
    
    def GetCreateArgs( self ):
        pandaPath = pm.Filename.fromOsSpecific( inspect.getfile( self.data.__class__ ) )
        
        relPath = pm.Filename( pandaPath )
        index = relPath.findOnSearchpath( pm.getModelPath().getValue() )
        if index >= 0:
            basePath = pm.getModelPath().getDirectories()[index]
            relPath.makeRelativeTo( basePath )
        
        return {'filePath':str( relPath )}