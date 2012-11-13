import xml.etree.ElementTree as et

import pandac.PandaModules as pm

import p3d
import game
import utils


class SceneParser( game.SceneParser ):
    
    def __init__( self, *args, **kwargs ):
        game.SceneParser.__init__( self, *args, **kwargs )
        
        self.saveCastFnMap = {
            bool:str,
            float:str,
            int:str,
            str:str,
            type:self.GetName,
            pm.Vec2:p3d.FloatTuple2Str,
            pm.LVecBase2f:p3d.FloatTuple2Str,
            pm.Vec3:p3d.FloatTuple2Str,
            pm.LVecBase3f:p3d.FloatTuple2Str,
            pm.Vec4:p3d.FloatTuple2Str,
            pm.LVecBase4f:p3d.FloatTuple2Str,
            pm.Point2:p3d.FloatTuple2Str,
            pm.Point3:p3d.FloatTuple2Str,
            pm.Point4:p3d.FloatTuple2Str,
            pm.Mat4:p3d.Mat42Str,
            pm.LMatrix4f:p3d.Mat42Str
        }
        
    def GetName( self, ttype ):
        return ttype.__name__
    
    def SaveData( self, wrpr, elem ):
        
        # Get a dictionary representing all the data for the component then
        # serialise it.
        dataDict = wrpr.GetData()
        for key, value in dataDict.items():
            if type( value ) in self.saveCastFnMap:
                castFn = self.saveCastFnMap[type( value )]
                subElem = et.SubElement( elem, 'Item' )
                subElem.set( 'name', key )
                subElem.set( 'value', castFn( value ) )
                subElem.set( 'type', type( value ).__name__ )
            else:
                print 'Could not save attribute: ', key, ' : of type: ', type( value )
                
        # Do child components
        for cWrpr in wrpr.children:
            cElem = et.SubElement( elem, 'Component' )
            cElem.set( 'type', cWrpr.name )
            for key, value in cWrpr.createArgs.items():
                cElem.set( key, value )
            self.SaveData( cWrpr, cElem )
    
    def SaveNode( self, np, parentElem ):
        """
        TO DO: Remove dependency on 'P3D_PickableNode' tag.
        """
        if np.getPythonTag( 'P3D_PickableNode' ):
            
            # Get the wrapper for this node type
            Wrpr = base.game.nodeMgr.GetWrapper( np )
            if Wrpr is not None:
                
                wrpr = Wrpr( np )
            
                # Create new element for this node path
                elem = et.SubElement( parentElem, 'Component' )
                
                # Write out node type and uuid.
                nTypeStr = base.game.nodeMgr.GetTypeString( np )
                elem.set( 'type', nTypeStr )
                
                # Write out create args
                for key, value in wrpr.createArgs.items():
                    elem.set( key, value )
                
                # Recursively save the data.
                self.SaveData( wrpr, elem )
            
        else:
            elem = parentElem
        
        # Recurse down the tree but ignore model root children, as serialising
        # them will load them twice.
        cElem = et.SubElement( elem, 'Children' )
        if type( np.node() ) != pm.ModelRoot:
            for childNp in np.getChildren():
                self.SaveNode( childNp, cElem )
            
        # Delete child elements if they're empty.
        if not list( cElem ) and not cElem.keys():
            elem.remove( cElem )
            
    def Save( self, rootNp, filePath ):
        """Save the scene out to an xml file."""
        # Create root element and version info
        rootElem = et.Element( 'Map' )
        self.SaveNode( rootNp, rootElem )
        
        # Wrap with an element tree and write to file
        tree = et.ElementTree( rootElem )
        utils.Indent( tree.getroot() )
        tree.write( filePath )