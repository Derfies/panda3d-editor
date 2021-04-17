import xml.etree.ElementTree as et


class SceneParser(object):
    
    """A class to load map files into Panda3D."""
    
    def load(self, rootNp, filePath):
        """Load the scene from an xml file."""
        self.nodes = {}
        self.cnctns = {}
        
        tree = et.parse(filePath)
        sRootElem = tree.find(".//Component[@type='SceneRoot']")
        self.load_component(sRootElem, None)
            
        # Load connections
        self.load_connections()
        
    def get_create_kwargs(self, wrprCls, elem):
        kwargs = {}
        
        for attr in wrprCls(None).create_attributes:
            pElem = elem.find(".//Item[@name='" + attr.name + "']")
            if pElem is not None:
                kwargs[attr.init_arg_name] = pElem.get('value')
                
        return kwargs
            
    def load_component(self, elem, pComp):
        wrprCls = base.node_manager.GetWrapperByName(elem.get('type'))
        if wrprCls is not None:
            
            args = self.get_create_kwargs(wrprCls, elem)
            if 'path' in elem.attrib:
                args['parent'] = pComp
                args['path'] = elem.attrib['path']
            
            # Create the node and load it`s properties.
            wrpr = wrprCls.create(**args)
            if pComp is not None:
                try:
                    print(wrpr, wrpr.__class__.mro())
                    wrpr.parent = pComp
                except:
                    print(wrpr, wrpr.parent, pComp)
                    raise

            wrpr.id = elem.get('id')
            self.nodes[id] = wrpr.data
            self.load_properties(wrpr, elem)
            
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
                self.load_component(cElem, wrpr)
            
    def load_properties(self, wrpr, elem):
        
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
        
        wrpr.set_property_data(propDict)
        
    def load_connections(self):
        for comp, cnctn in self.cnctns.items():
            
            # Swap uuids for NodePaths
            cnctnDict = {}
            for key, vals in cnctn.items():
                for val in vals:
                    if val in self.nodes:
                        cnctnDict.setdefault(key, [])
                        cnctnDict[key].append(self.nodes[val])
            
            wrpr = base.node_manager.wrap(comp)
            wrpr.set_connection_data(cnctnDict)