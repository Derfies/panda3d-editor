import inspect

from .constants import *


WRAPPER_MODULE_NAMES = [
    'base',
    'sceneRoot',
    
    'pandaNode',
    'nodePath',
    'modelNode',
    'camera',
    'showbaseDefault',
    'modelRoot',
    'actor',
    'fog',
    
    'collisionNode',
    'collisionSolids',

    'light',
    'ambientLight',
    'pointLight',
    'directionalLight',
    'spotlight',
    
    'texture',
    'textureStage',
    
    'bulletWorld',
    'bulletDebugNode',
    'bulletRigidBodyNode',
    'bulletCharacterControllerNode',
    'bulletBoxShape',
    'bulletPlaneShape',
    'bulletCapsuleShape'
]


from importlib import import_module

class Manager( object ):
    
    def __init__( self ):
        self.nodeWrappers = {}
        
        # Load component wrapper classes from the list of module names and 
        # store them in the nodeWrapper dictionary. This needs to be done when
        # this class is instantiated - not when the module is imported - so
        # the editor classes are loaded beforehand.
        for modName in WRAPPER_MODULE_NAMES:
            mod = import_module('pandaEditor.game.nodes.' + modName)
            for mem in inspect.getmembers( mod, inspect.isclass ):
                cls = mem[1]
                if cls.__module__ == mod.__name__:
                    self.nodeWrappers[cls.__name__] = cls
        
    def Create( self, nTypeStr, *args ):
        wrprCls = self.nodeWrappers[nTypeStr]
        return wrprCls.Create( *args )
    
    def Wrap( self, comp ):
        """
        Return a wrapper suitable for the indicated component. If the correct
        wrapper cannot be found, return a NodePath wrapper for NodePaths and
        a Base wrapper for everything else.
        """
        wrprCls = self.GetWrapper( comp )
        if wrprCls is not None:
            return wrprCls( comp )
        else:
            wrprCls = self.GetDefaultWrapper( comp )
            return wrprCls( comp )
        
    def GetDefaultWrapper( self, comp ):
        if hasattr( comp, 'getPythonTag' ):
            return self.nodeWrappers['NodePath']
        else:
            return self.nodeWrappers['Base']
        
    def GetCommonWrapper( self, comps ):
        
        # Get method resolution orders for each wrapper for all the indicated
        # components.
        mros = []
        for comp in comps:
            wrprCls = self.GetWrapper( comp )
            if wrprCls is not None:
                mros.append( wrprCls.mro() )
                
        if not mros:
            return self.GetDefaultWrapper( comps[0] )
                
        # Intersect the mros to get the common classes.
        cmnClasses = set( mros[0] ).intersection( *mros )
        
        # The result was unordered, so go find the first common class from
        # one of the mros.
        for cls in mros[0]:
            if cls in cmnClasses:
                return cls
        
    def GetWrapper( self, comp ):
        typeStr = self.GetTypeString( comp )
        if typeStr in self.nodeWrappers:
            return self.nodeWrappers[typeStr]
        
        return None
    
    def GetWrapperByName( self, cType ):
        if cType in self.nodeWrappers:
            return self.nodeWrappers[cType]
        
        return None
        
    def GetTypeString( self, comp ):
        """
        Return the type of the component as a string. Components are 
        identified in the following method (in order):
        
        - If the component has the class variable 'cType' then this string
        will be used as the type.
        - Use the component's type's name as the type.
        - If this is 'NodePath' then look for a overriding tag on the node
        for the type.
        - If this tag is missing, use the NodePath's node as the type.
        """
        if hasattr( comp.__class__, 'cType' ):
            return comp.cType
        
        typeStr = type( comp ).__name__
        if typeStr == 'NodePath':
            typeStr = comp.node().getTag( TAG_NODE_TYPE )
            if not typeStr:
                typeStr = type( comp.node() ).__name__
                
        return typeStr