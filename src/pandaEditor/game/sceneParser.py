import xml.etree.ElementTree as et


class SceneParser(object):
    
    """A class to load map files into Panda3D."""
    
    def Load(self, rootNp, filePath):
        """Load the scene from an xml file."""
        self.nodes = {}
        self.cnctns = {}
        
        tree = et.parse(filePath)
        sRootElem = tree.find(".//Component[@type='SceneRoot']")
        self.LoadComponent(sRootElem, None)
            
        # Load connections
        self.LoadConnections()
        
    def GetCreateKwargs(self, wrprCls, elem):
        kwargs = {}
        
        for attr in wrprCls(None).GetCreateAttributes():
            pElem = elem.find(".//Item[@name='" + attr.name + "']")
            if pElem is not None:
                kwargs[attr.initName] = pElem.get('value')
                
        return kwargs
            
    def LoadComponent(self, elem, pComp):
        wrprCls = base.game.nodeMgr.GetWrapperByName(elem.get('type'))
        if wrprCls is not None:
            
            args = self.GetCreateKwargs(wrprCls, elem)
            if 'path' in elem.attrib:
                args['parent'] = pComp
                args['path'] = elem.attrib['path']
            
            # Create the node and load its properties.
            wrpr = wrprCls.Create(**args)
            wrpr.SetParent(pComp)
            
            id = elem.get('id')
            wrpr.SetId(id)
            self.nodes[id] = wrpr.data
            self.LoadProperties(wrpr, elem)
            
            # Store connections so we can set them up once the rest of
            # the scene has been loaded.
            cnctnsElem = elem.find('Connections')
            if cnctnsElem is not None:
                cnctnDict = {}
                for cnctnElem in cnctnsElem:
                    cType = cnctnElem.get('type')
                    uuid = cnctnElem.get('value')
                    cnctnDict.setdefault(cType, [])
                    cnctnDict[cType].append(uuid)
                self.cnctns[wrpr.data] = cnctnDict
            
            # Recurse through hierarchy.
            for cElem in elem.findall('Component'):
                self.LoadComponent(cElem, wrpr.data)
            
    def LoadProperties(self, wrpr, elem):
        
        # Pull all properties from the xml for this component, then get the 
        # wrapper and set all of them.
        propElems = elem.findall('Item')
        propDict = {}
        for propElem in propElems:
            cElems = propElem.findall('Item')
            if not cElems:
                propDict[propElem.get('name')] = propElem.get('value')
            else:
                itemDict = {}
                for itemElem in cElems:
                    itemDict[itemElem.get('name')] = itemElem.get('value')
                propDict[propElem.get('name')] = itemDict
        
        wrpr.SetPropertyData(propDict)
        
    def LoadConnections(self):
        for comp, cnctn in self.cnctns.items():
            
            # Swap uuids for NodePaths
            cnctnDict = {}
            for key, vals in cnctn.items():
                for val in vals:
                    if val in self.nodes:
                        cnctnDict.setdefault(key, [])
                        cnctnDict[key].append(self.nodes[val])
            
            wrpr = base.game.nodeMgr.Wrap(comp)
            wrpr.SetConnectionData(cnctnDict)