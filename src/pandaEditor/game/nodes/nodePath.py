import uuid

import pandac.PandaModules as pm
from pandac.PandaModules import NodePath as NP

from base import Base
from constants import *
from attributes import NodePathAttribute as Attr


class NodePath( Base ):
    
    def __init__( self, *args, **kwargs ):
        nType = kwargs.pop( 'nType', None )
        Base.__init__( self, *args, **kwargs )
        
        # Generate a default name from the node type.
        self.type = nType
        if self.type is not None:
            nodeName = self.type.__name__
            self.nodeName = nodeName[0:1].lower() + nodeName[1:]
        
        pAttr = Attr( 'NodePath' )
        pAttr.children.extend( 
            [
                Attr( 'Name', str, NP.getName, NP.setName ),
                Attr( 'Matrix', pm.Mat4, NP.getMat, NP.setMat ),
                Attr( 'Uuid', str, NP.getTag, NP.setTag, None, [TAG_NODE_UUID], [TAG_NODE_UUID], e=False )
            ]
        )
        self.attributes.append( pAttr )
        
    def SetupNodePath( self, np ):
        id = str( uuid.uuid4() )
        np.setTag( TAG_NODE_UUID, id )
            
    def Create( self ):
        """
        Create a NodePath with the indicated type and name, set it up and
        return it.
        """
        np = pm.NodePath( self.type( self.nodeName ) )
        self.SetupNodePath( np )
        self.Wrap( np )
        return pm.NodePath( np )
    
    def Duplicate( self, np, dupeNp ):
        Base.Duplicate( self, np, dupeNp )
        
        for child in self.children:
            child.Duplicate( np, dupeNp )
        base.game.pluginMgr.OnNodeDuplicate( self.data )
    
    def Destroy( self ):
        Base.Destroy( self )
        
        for child in self.children:
            child.Destroy()
        base.game.pluginMgr.OnNodeDestroy( self.data )
    
    def GetChildWrapper( self, name ):
        
        if name in base.game.nodeMgr.pyTagWrappers:
            return base.game.nodeMgr.pyTagWrappers[name]
        
        return None
    
    def GetTags( self ):
        tags = self.data.getPythonTag( TAG_PYTHON_TAGS )
        if tags is not None:
            return [tag for tag in tags if tag in base.game.nodeMgr.pyTagWrappers]
        
        return []
            
    def Wrap( self, np ):
        Base.Wrap( self, np )
        
        # Wrap python objects
        tags = self.GetTags()
        for tag in tags:
            pyObj = np.getPythonTag( tag )
            pyObjWrpr = base.game.nodeMgr.pyTagWrappers[tag]
            wrpr = pyObjWrpr( pyObj )
            self.children.append( wrpr )