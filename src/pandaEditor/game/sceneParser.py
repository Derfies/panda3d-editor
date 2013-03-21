import panda3d.core as pc
import xml.etree.ElementTree as et

import p3d


class SceneParser( object ):
    
    """A class to load map files into Panda3D."""
    
    def __init__( self ):
        self.loadCastFnMap = {
            'bool':p3d.Str2Bool,
            'float':float,
            'int':int,
            'str':str,
            'unicode':str,
            'LVector2f':p3d.Str2Vec2,
            'LVecBase2f':p3d.Str2Vec2,
            'LVector3f':p3d.Str2Vec3,
            'LVecBase3f':p3d.Str2Vec3,
            'LVector4f':p3d.Str2Vec4,
            'LVecBase4f':p3d.Str2Vec4,
            'LPoint3f':p3d.Str2Point3,
            'LMatrix4f':p3d.Str2Mat4,
            'Filename':str
        }
    
    def Load( self, rootNp, filePath ):
        """Load the scene from an xml file."""
        self.nodes = {}
        self.cnctns = {}
        
        tree = et.parse( filePath )
        sRootElem = tree.find( ".//Component[@type='SceneRoot']" )
        self.LoadComponent( sRootElem, None )
            
        # Load connections
        self.LoadConnections()
            
    def LoadComponent( self, elem, pComp ):
        wrprCls = base.game.nodeMgr.GetWrapperByName( elem.get( 'type' ) )
        if wrprCls is not None:
            
            # Get all arguments needed to create the node including the 
            # parent.
            args = self.GetCreateArgs( elem.attrib )
            args['parent'] = pComp
            
            # Create the node and load its properties.
            wrpr = wrprCls.Create( **args )
            wrpr.SetParent( pComp )
            
            id = elem.get( 'id' )
            wrpr.SetId( id )
            self.nodes[id] = wrpr.data
            self.LoadProperties( wrpr, elem )
            
            # Store connections so we can set them up once the rest of
            # the scene has been loaded.
            cnctnsElem = elem.find( 'Connections' )
            if cnctnsElem is not None:
                cnctnDict = {}
                for cnctnElem in cnctnsElem:
                    cType = cnctnElem.get( 'type' )
                    uuid = cnctnElem.get( 'value' )
                    cnctnDict.setdefault( cType, [] )
                    cnctnDict[cType].append( uuid )
                self.cnctns[wrpr.data] = cnctnDict
            
        # Recurse through hierarchy.
        for cElem in elem.findall( 'Component' ):
            self.LoadComponent( cElem, wrpr.data )
            
    def GetCreateArgs( self, attrib ):
        createArgs = attrib.copy()
        createArgs.pop( 'id', None )
        createArgs.pop( 'type' )
        return createArgs
            
    def LoadProperties( self, wrpr, elem ):
        
        # Pull all properties from the xml for this component, then get the 
        # wrapper and set all of them.
        propElems = elem.findall( 'Item' )
        propDict = {}
        for propElem in propElems:
            propType = propElem.get( 'type' )
            if propType in self.loadCastFnMap:
                castFn = self.loadCastFnMap[propType]
                propDict[propElem.get( 'name' )] = castFn( propElem.get( 'value' ) )
            elif propType == 'dict':
                itemDict = {}
                for itemElem in propElem.findall( 'Item' ):
                    castFn = self.loadCastFnMap[itemElem.get( 'type' )]
                    itemDict[itemElem.get( 'name' )] = castFn( itemElem.get( 'value' ) )
                propDict[propElem.get( 'name' )] = itemDict
            else:
                print 'Could not load attribute: ', propElem.get( 'name' ), ' : of type: ', propType
        
        wrpr.SetPropertyData( propDict )
        
    def LoadConnections( self ):
        for comp, cnctn in self.cnctns.items():
            
            # Swap uuids for NodePaths
            cnctnDict = {}
            for key, vals in cnctn.items():
                for val in vals:
                    if val in self.nodes:
                        cnctnDict.setdefault( key, [] )
                        cnctnDict[key].append( self.nodes[val] )
            
            wrpr = base.game.nodeMgr.Wrap( comp )
            wrpr.SetConnectionData( cnctnDict )