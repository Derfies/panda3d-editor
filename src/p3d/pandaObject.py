import os
import imp
import sys
import inspect

from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject

import p3d


TAG_PANDA_OBJECT = 'PandaObject'


class PandaObject( object ):
    
    """
    Basic building block class, designed to be attached to a node path in the
    scene graph. Doing this creates a circular reference, so care must be
    taken to clear the python tag on this class' node path before trying to
    remove it.
    """
    
    def __init__( self, np ):
        
        # Store the node path with a reference to this class attached to it
        self.np = np
        self.np.setPythonTag( TAG_PANDA_OBJECT, self )
        
        self.actor = False
        self.instances = {}
        
    def __del__( self ):
        print TAG_PANDA_OBJECT, ' : ', self.np.getName(), ' DELETED'
        
    @staticmethod
    def Get( np ):
        
        # Return the panda object for the supplied node path
        return np.getPythonTag( TAG_PANDA_OBJECT )
    
    @staticmethod
    def Break( np ):
        
        # Detach each script from the object
        pObj = PandaObject.Get( np )
        if pObj is not None and hasattr( pObj, 'instances' ):
            for clsName in pObj.instances.keys():
                pObj.DetachScript( clsName )
        
        # Clear the panda object tag to allow for proper garbage collection
        np.clearPythonTag( TAG_PANDA_OBJECT )
        
    @classmethod
    def Duplicate( cls, np ):
        
        # Get the panda object for the input node path
        pObj = np.getPythonTag( TAG_PANDA_OBJECT )
        if pObj is None:
            return None
        
        # Duplicate the panda object then iterate over the attached instances
        # and recreate them on the duplicate
        dupePObj = cls( np )
        for instance in pObj.instances.values():
            instance = dupePObj.AttachScript( inspect.getfile( instance.__class__ ) )
            clsName = instance.__class__.__name__
            
            # Copy property values over
            for propName in pObj.GetInstanceProperties( instance ):
                value = getattr( instance, propName )
                setattr( dupePObj.instances[clsName], propName, value )
            
        return dupePObj
        
    def AttachScript( self, filePath ):
        
        # Make sure we're dealing with forward slashes 
        filePath = filePath.replace( '\\', '/' )
        
        # Get the name of the module
        filePath = os.path.normpath( filePath )
        head, tail = os.path.split( filePath )
        name = os.path.splitext( tail )[0]
        
        # If the script path is not absolute then we'll need to search for it.
        # imp.find_module won't take file paths so create a list of search
        # paths by joining the tail of file path to each path in sys.path.
        mod = None
        dirPath = os.path.split( filePath )[0]
        if not os.path.isabs( filePath ):
            for sysPath in sys.path:
                testPath = os.path.join( sysPath, dirPath )
                sys.path.insert( 0, testPath )
                print 'testing: ', name, ' : ', testPath
                
                try:
                    #if name in sys.modules:
                    #    del name
                    mod = __import__( name )
                    reload( mod ) # Might need to refresh...
                except:
                    pass
                finally:
                    sys.path.pop( 0 )
                    
                print 'MOD: ', mod
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
        self.instances[clsName] = instance
        
        # Set some basic attributes
        setattr( cls, 'np', self.np )
        
        # Register the script path with the panda manager. Use inspect to make
        # sure we get the full script path instead of a relative path.
        #scriptPath = inspect.getfile( instance.__class__ )
        #p3d.PandaManager().RegisterScript( scriptPath, self )
        
        return instance
    
    def DetachScript( self, clsName ):
        
        # Remove an instance from the instance dictionary by its class name. 
        # Make sure to call ignoreAll() on all instances attached to this 
        # object which inherit from DirectObject or else they won't be 
        # deleted properly.
        if clsName in self.instances:
            instance = self.instances[clsName]
            if isinstance( instance, DirectObject ):
                instance.ignoreAll()
            del self.instances[clsName]
            
    def ReloadScript( self, scriptPath ):
    
        # Get the class name
        head, tail = os.path.split( scriptPath )
        name = os.path.splitext( tail )[0]
        clsName = name[0].upper() + name[1:]
        
        # Get the old instance
        oldInst = self.instances[clsName]
        
        # Remove the old object and recreate it
        self.DetachScript( clsName )
        self.AttachScript( scriptPath )
        
        # Go through the old instance properties and set them on the
        # new instance
        newInst = self.instances[clsName]
        for pName, pType in self.GetInstanceProperties( oldInst ).items():
            pValue = getattr( oldInst, pName )
            setattr( newInst, pName, pValue )
                    
    def GetInstanceProperties( self, instance ):
        
        # Return a dictionary with keys being the name of the property, and
        # values the actual property
        props = {}
        
        for propName, prop in vars( instance.__class__ ).items():
            if type( prop ) == type:
                props[propName] = prop
                
        return props
            
    def CreateActor( self ):
        
        # Turn the node path into an actor
        actor = Actor( self.np )
        actor.reparentTo( self.np.getParent() )
        actor.setTransform( self.np.getTransform() )
        actor.setPythonTag( TAG_PANDA_OBJECT, self )
        
        # Fix scripts to point to the new actor node path
        for script in self.instances.values():
            script.np = actor
        
        # Clear and detach old node path
        self.np.clearPythonTag( TAG_PANDA_OBJECT )
        self.np.detachNode()
        
        # Get the file path to the model
        self.actorFilePath = str( self.np.node().getFullpath() )
        
        self.np = actor
        self.actor = True
        
        return self.np