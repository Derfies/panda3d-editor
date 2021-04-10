import inspect
from importlib import import_module

from pandaEditor.game.nodes.constants import *


GAME_NODE_MODULES = [
    'pandaEditor.game.nodes.base',
    'pandaEditor.game.nodes.sceneRoot',
    
    'pandaEditor.game.nodes.pandaNode',
    'pandaEditor.game.nodes.nodePath',
    'pandaEditor.game.nodes.modelNode',
    'pandaEditor.game.nodes.camera',
    'pandaEditor.game.nodes.showbaseDefault',
    'pandaEditor.game.nodes.modelRoot',
    'pandaEditor.game.nodes.actor',
    'pandaEditor.game.nodes.fog',
    
    'pandaEditor.game.nodes.collisionNode',
    'pandaEditor.game.nodes.collisionSolids',

    'pandaEditor.game.nodes.light',
    'pandaEditor.game.nodes.ambientLight',
    'pandaEditor.game.nodes.pointLight',
    'pandaEditor.game.nodes.directionalLight',
    'pandaEditor.game.nodes.spotlight',
    
    'pandaEditor.game.nodes.texture',
    'pandaEditor.game.nodes.textureStage',
    
    'pandaEditor.game.nodes.bulletWorld',
    'pandaEditor.game.nodes.bulletDebugNode',
    'pandaEditor.game.nodes.bulletRigidBodyNode',
    'pandaEditor.game.nodes.bulletCharacterControllerNode',
    'pandaEditor.game.nodes.bulletBoxShape',
    'pandaEditor.game.nodes.bulletPlaneShape',
    'pandaEditor.game.nodes.bulletCapsuleShape'
]


class Manager:
    
    def __init__(self):
        self.nodeWrappers = {}

        self.create_node_wrappers(GAME_NODE_MODULES)

    def create_node_wrappers(self, module_paths):
        for module_path in module_paths:
            module = import_module(module_path)
            for member in inspect.getmembers(module, inspect.isclass):
                cls = member[1]
                if cls.__module__ == module.__name__:
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
        
    def GetWrapper(self, comp):
        type_ = self.GetTypeString(comp)
        return self.nodeWrappers.get(type_)
    
    def GetWrapperByName(self, c_type):
        return self.nodeWrappers.get(c_type)
        
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