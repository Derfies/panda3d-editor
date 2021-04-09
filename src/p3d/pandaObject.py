import os
import imp
import sys
import inspect

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
    def __init__( self ):
        self.instances = {}
        
    def __del__( self ):
        print(TAG_PANDA_OBJECT, ' : ', self.np.getName(), ' DELETED')
        
    def AttachToNodePath( self, np ):
        self.np = np
        self.np.setPythonTag( TAG_PANDA_OBJECT, self )
        
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