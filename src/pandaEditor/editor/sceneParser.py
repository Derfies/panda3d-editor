import xml.etree.ElementTree as et

import panda3d.core as pc
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
            pm.LMatrix4f:p3d.Mat42Str,
            pc.Filename:str
        }
        
    def GetName( self, ttype ):
        return ttype.__name__
    
    def Save( self, scene, filePath ):
        """Save the scene out to an xml file."""
        rootElem = et.Element( 'Scene' )
        wrpr = base.game.nodeMgr.Wrap( scene )
        self.SaveComponent( wrpr, rootElem )
        
        # Wrap with an element tree and write to file.
        tree = et.ElementTree( rootElem )
        utils.Indent( tree.getroot() )
        tree.write( filePath )
    
    def SaveComponent( self, wrpr, pElem, name='Component' ):
        """Serialise a component to an xml element."""
        elem = pElem
        if wrpr.IsSaveable():
            elem = et.SubElement( pElem, name )
            elem.set( 'type', type( wrpr ).__name__ )
            id = wrpr.GetId()
            if id is not None:
                elem.set( 'id', id )
            for key, value in wrpr.GetCreateArgs().items():
                elem.set( key, value )
            self.SaveProperties( wrpr, elem )
            self.SaveConnections( wrpr, elem )
        
        # Write out addons.
        for cWrpr in wrpr.GetAddons():
            self.SaveComponent( cWrpr, elem )
        
        # Recurse through hierarchy.
        for cWrpr in wrpr.GetChildren():
            self.SaveComponent( cWrpr, elem )
                
    def SaveProperties( self, wrpr, elem ):
        """
        Get a dictionary representing all the properties for the component
        then serialise it.
        """
        propDict = wrpr.GetPropertyData()
        for key, value in propDict.items():
            if type( value ) in self.saveCastFnMap:
                castFn = self.saveCastFnMap[type( value )]
                subElem = et.SubElement( elem, 'Item' )
                subElem.set( 'name', key )
                subElem.set( 'value', castFn( value ) )
                subElem.set( 'type', type( value ).__name__ )
            elif type( value ) == dict:
                subElem = et.SubElement( elem, 'Item' )
                subElem.set( 'name', key )
                subElem.set( 'type', 'dict' )
                for key, val in value.items():
                    subElem.append( self.SaveItem( key, val ) )
            else:
                print 'Could not save attribute: ', key, ' : of type: ', type( value )
                
    def SaveItem( self, name, value ):
        castFn = self.saveCastFnMap[type( value )]
        elem = et.Element( 'Item' )
        elem.set( 'name', name )
        elem.set( 'type', type( value ).__name__ )
        elem.set( 'value', castFn( value ) )
        return elem
                
    def SaveConnections( self, wrpr, elem ):
        cnctnDict = wrpr.GetConnectionData()
        if not cnctnDict:
            return
        
        cnctnsElem = et.Element( 'Connections' )
        for key, vals in cnctnDict.items():
            for val in vals:
                cnctnElem = et.SubElement( cnctnsElem, 'Connection' )
                cnctnElem.set( 'type', key )
                cnctnElem.set( 'value', val )
                
        # Append the connections element only if it isn't empty.
        if list( cnctnsElem ):
            elem.append( cnctnsElem )