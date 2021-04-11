import inspect
from importlib import import_module

from panda3d.core import ConfigVariableBool

from game.nodes.constants import TAG_NODE_TYPE


GAME_NODE_MODULES = [
    'game.nodes.base',
    'game.nodes.sceneRoot',
    
    'game.nodes.pandaNode',
    'game.nodes.nodePath',
    'game.nodes.modelNode',
    'game.nodes.camera',
    'game.nodes.showbaseDefault',
    'game.nodes.modelRoot',
    'game.nodes.actor',
    'game.nodes.fog',
    
    'game.nodes.collisionNode',
    'game.nodes.collisionSolids',

    'game.nodes.light',
    'game.nodes.ambientLight',
    'game.nodes.pointLight',
    'game.nodes.directionalLight',
    'game.nodes.spotlight',
    
    'game.nodes.texture',
    'game.nodes.textureStage',
    
    'game.nodes.bulletWorld',
    'game.nodes.bulletDebugNode',
    'game.nodes.bulletRigidBodyNode',
    'game.nodes.bulletCharacterControllerNode',
    'game.nodes.bulletBoxShape',
    'game.nodes.bulletPlaneShape',
    'game.nodes.bulletCapsuleShape'
]


cache = {}


def import_wrapper(full_module_path):
    if full_module_path in cache:
        return cache[full_module_path]
    editor_mode = ConfigVariableBool('editor_mode', False)
    prefix = 'editor' if editor_mode else 'game'
    module_path, class_name = full_module_path.rsplit('.', 1)
    module = import_module(f'{prefix}.{module_path}')
    members = iter([
        value
        for name, value in inspect.getmembers(module, inspect.isclass)
        if name == class_name
    ])
    cls = next(members, None)
    if cls is not None:
        cache[module_path] = cls
        return cls
    raise ModuleNotFoundError(f'No module found at: {full_module_path}')


class Manager:
    
    def __init__(self):
        self.wrappers = {}
        self.create_node_wrappers(GAME_NODE_MODULES)

    def create_node_wrappers(self, module_paths):
        for module_path in module_paths:
            module = import_module(module_path)
            for member in inspect.getmembers(module, inspect.isclass):
                cls = member[1]
                if cls.__module__ == module.__name__:
                    self.wrappers[cls.__name__] = cls
        
    def Create(self, nTypeStr, *args):
        wrprCls = self.wrappers[nTypeStr]
        return wrprCls.Create(*args)
    
    def Wrap(self, comp):
        """
        Return a wrapper suitable for the indicated component. If the correct
        wrapper cannot be found, return a NodePath wrapper for NodePaths and
        a Base wrapper for everything else.
        """
        wrprCls = self.GetWrapper(comp)
        if wrprCls is not None:
            return wrprCls(comp)
        else:
            wrprCls = self.GetDefaultWrapper(comp)
            return wrprCls(comp)
        
    def GetDefaultWrapper(self, comp):
        if hasattr(comp, 'getPythonTag'):
            return self.wrappers['NodePath']
        else:
            return self.wrappers['Base']
        
    def GetCommonWrapper(self, comps):
        
        # Get method resolution orders for each wrapper for all the indicated
        # components.
        mros = []
        for comp in comps:
            wrprCls = self.GetWrapper(comp)
            if wrprCls is not None:
                mros.append(wrprCls.mro())
                
        if not mros:
            return self.GetDefaultWrapper(comps[0])
                
        # Intersect the mros to get the common classes.
        cmnClasses = set(mros[0]).intersection(*mros)
        
        # The result was unordered, so go find the first common class from
        # one of the mros.
        for cls in mros[0]:
            if cls in cmnClasses:
                return cls
        
    def GetWrapper(self, comp):
        type_ = self.GetTypeString(comp)
        return self.wrappers.get(type_)
    
    def GetWrapperByName(self, c_type):
        return self.wrappers.get(c_type)
        
    def GetTypeString(self, comp):
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
        if hasattr(comp.__class__, 'cType'):
            return comp.cType
        
        typeStr = type(comp).__name__
        if typeStr == 'NodePath':
            typeStr = comp.node().getTag(TAG_NODE_TYPE)
            if not typeStr:
                typeStr = type(comp.node()).__name__
                
        return typeStr