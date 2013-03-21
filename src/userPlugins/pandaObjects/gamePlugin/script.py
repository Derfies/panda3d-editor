import os
import sys
import inspect

import p3d
from pandaObject import PandaObjectNPO
from game.nodes.base import Base


class Script( Base ):
    
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
        instance = class_( clsName )
        
        return cls( instance )
    
    def Detach( self ):
        
        # Find the script in the list of instances for this PandaObject and
        # remove it.
        pObj = PandaObjectNPO.Get( self.data.np )
        for name, inst in pObj.instances.items():
            if inst == self.data:
                del pObj.instances[name]
                return
            
    def SetId( self, id ):
        
        # Scripts don't need ids.
        pass
        
    def GetParent( self ):
        np = p3d.PandaObject.Get( self.data.np )
        return base.game.nodeMgr.Wrap( np )
        
    def SetParent( self, pObj ):
        if pObj is not None:
            name = self.GetFileName( inspect.getfile( self.data.__class__ ) )
            clsName = name[0].upper() + name[1:]
            pObj.instances[clsName] = self.data
            self.data.np = pObj.np
            
    @staticmethod
    def GetFileName( filePath ):
        normPath = os.path.normpath( filePath )
        head, tail = os.path.split( normPath )
        return os.path.splitext( tail )[0]
    
    def SetPropertyData( self, dataDict ):
        
        # Set the instance variables from the supplied dictionary.
        for key, value in dataDict.items():
            setattr( self.data, key, value )