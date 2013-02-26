import uuid

import pandac.PandaModules as pm
from pandac.PandaModules import NodePath as NP

from base import Base
from constants import *
from attributes import NodePathAttribute as Attr
from game.nodes.connections import Connection as Cnnctn
from game.nodes.connections import ConnectionList as CnnctnList


class NodePath( Base ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', NP )
        Base.__init__( self, *args, **kwargs )
        
        self.initArgs = [self.nodeName]
        
        pAttr = Attr( 'NodePath' )
        pAttr.children.extend( 
            [
                Attr( 'Name', str, NP.getName, NP.setName ),
                Attr( 'Matrix', pm.Mat4, NP.getMat, NP.setMat ),
                CnnctnList( 'Light', pm.Light, self.GetLights, NP.setLight, NP.clearLight, NP.clearLight, self.data ),
                Cnnctn( 'Texture', pm.Texture, NP.getTexture, NP.setTexture, NP.clearTexture, self.data, [1] )
            ]
        )
        self.attributes.append( pAttr )
        
    def GetLights( self, data ):
        lgts = []
        
        lgtAttrib = data.getAttrib( pm.LightAttrib )
        if lgtAttrib is not None:
            lgts = lgtAttrib.getOnLights()
        
        return lgts
            
    def Create( self, *args, **kwargs ):
        """
        Create a NodePath with the indicated type and name, set it up and
        return it.
        """
        if 'path' not in kwargs:
            np = pm.NodePath( self.type( *self.initArgs ) )
            self.SetupNodePath( np )
        else:
            np = self.FindChild( kwargs['path'], kwargs['parent'] )
        self.data = np
        return np
    
    def Detach( self ):
        self.data.detachNode()
    
    def Destroy( self ):
        Base.Destroy( self )
        
        for child in self.children:
            child.Destroy()
        base.game.pluginMgr.OnNodeDestroy( self.data )
        
    def Duplicate( self, np, dupeNp ):
        Base.Duplicate( self, np, dupeNp )
        
        for child in self.children:
            child.Duplicate( np, dupeNp )
        base.game.pluginMgr.OnNodeDuplicate( self.data )
        
        # Give a new uuid to the duplicate node.
        self.SetupNodePath( dupeNp )
        
    def SetupNodePath( self, np ):
        id = str( uuid.uuid4() )
        np.setTag( TAG_NODE_UUID, id )
        
    def AddChild( self, np ):
        np.reparentTo( self.data )
        
    def FindChild( self, path, parent ):
        buffer = path.split( '|' )
        np = parent
        for elem in buffer:
            childNames = [child.getName() for child in np.getChildren()]
            index = childNames.index( elem )
            np = np.getChildren()[index]
                    
        return np