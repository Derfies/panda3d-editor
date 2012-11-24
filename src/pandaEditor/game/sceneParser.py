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
            'LVector2f':p3d.Str2FloatTuple,
            'LVecBase2f':p3d.Str2FloatTuple,
            'LVector3f':p3d.Str2FloatTuple,
            'LVecBase3f':p3d.Str2FloatTuple,
            'LVector4f':p3d.Str2FloatTuple,
            'LVecBase4f':p3d.Str2FloatTuple,
            'LPoint3f':p3d.Str2FloatTuple,
            'LMatrix4f':p3d.Str2Mat4
        }
        
    def GetCreateArgs( self, attrib ):
        attrib.pop( 'type' )
        return attrib
    
    def LoadData( self, wrpr, elem ):
        rtn = None
        
        # Pull all data from the xml for this component, then get the wrapper
        # to set the data.
        dataElems = elem.findall( 'Item' )
        dataDict = {}
        for dataElem in dataElems:
            dataType = dataElem.get( 'type' )
            if dataType in self.loadCastFnMap:
                castFn = self.loadCastFnMap[dataType]
                dataDict[dataElem.get( 'name' )] = castFn( dataElem.get( 'value' ) )
                
                # Keep a record of all uuids so we can set up connections 
                # later.
                if dataElem.get( 'name' ) == 'uuid':
                    rtn = dataElem.get( 'value' )
            else:
                print 'Could not load attribute: ', dataElem.get( 'name' ), ' : of type: ', dataType
        wrpr.SetData( dataDict )
        
        # Do child components
        cElems = elem.findall( 'Component' )
        for cElem in cElems:
            CWrpr = wrpr.GetChildWrapper( cElem.get( 'type' ) )
            if CWrpr is not None:
                cWrpr = CWrpr()
                cWrpr.Create( wrpr.data, **self.GetCreateArgs( cElem.attrib ) )
                return self.LoadData( cWrpr, cElem )
                
        return rtn
        
    def LoadNode( self, elem, parentNp ):
        """Build an element from xml."""
        # Build the node
        strType = elem.get( 'type' )
        if elem.tag == 'Component' and strType in base.game.nodeMgr.nodeWrappers:
            
            # Get the node type
            Wrpr = base.game.nodeMgr.GetWrapperByName( strType )
            if Wrpr is not None:
                
                # Create the base node path
                wrpr = Wrpr()
                np = wrpr.Create( **self.GetCreateArgs( elem.attrib ) )
                
                if parentNp is not None:
                    np.reparentTo( parentNp )
                    
                    if not hasattr( self, 'rootNp' ):
                        self.rootNp = parentNp
                
                # Load data for the node.
                self.nodes[self.LoadData( wrpr, elem )] = np
                
                # At this stage np might be an actor, so cast back to node path.
                # This may cause some weird issues. Not sure...
                np = np.anyPath( np.node() )   
                
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
                        self.cnctns[np] = cnctnDict
                
        else:
            np = parentNp
        
        # Recurse down the tree
        cElem = elem.find( 'Children' )
        if cElem is not None:
            for childElem in cElem:
                self.LoadNode( childElem, np )
                
    def LoadConnections( self ):

        for np, cnctn in self.cnctns.items():
            
            # Swap uuids for NodePaths
            cnctnDict = {}
            for key, vals in cnctn.items():
                for val in vals:
                    if val in self.nodes:
                        cnctnDict.setdefault( key, [] )
                        cnctnDict[key].append( self.nodes[val] )
            
            wrpr = base.game.nodeMgr.Wrap( np )
            wrpr.SetConnections( cnctnDict )
            
    def Load( self, rootNp, filePath ):
        """Load the scene from an xml file."""
        self.nodes = {}
        self.cnctns = {}
        
        tree = et.parse( filePath )
        # DEBUG
        if rootNp is render:
            rootNp = None
        for child in tree.getroot():
            self.LoadNode( child, rootNp )
            
        # Load connections
        self.LoadConnections()