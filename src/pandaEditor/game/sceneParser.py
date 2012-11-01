import xml.etree.cElementTree as et

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
        
        # Pull all data from the xml for this component, then get the wrapper
        # to set the data.
        dataElems = elem.findall( 'Item' )
        dataDict = {}
        for dataElem in dataElems:
            dataType = dataElem.get( 'type' )
            if dataType in self.loadCastFnMap:
                castFn = self.loadCastFnMap[dataType]
                dataDict[dataElem.get( 'name' )] = castFn( dataElem.get( 'value' ) )
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
                self.LoadData( cWrpr, cElem )
        
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
                np.reparentTo( parentNp )
                
                # Load data for the node.
                self.LoadData( wrpr, elem )
                
                # At this stage np might be an actor, so cast back to node path.
                # This may cause some weird issues. Not sure...
                np = np.anyPath( np.node() )     
                
        else:
            np = parentNp
        
        # Recurse down the tree
        cElem = elem.find( 'Children' )
        if cElem is not None:
            for childElem in cElem:
                self.LoadNode( childElem, np )
            
    def Load( self, rootNp, filePath ):
        """Load the scene from an xml file."""
        tree = et.parse( filePath )
        self.LoadNode( tree.getroot(), rootNp )