import logging
import xml.etree.ElementTree as et
from direct.showbase.PythonUtil import getBase as get_base

from p3d.commonUtils import unserialise


logger = logging.getLogger(__name__)


class SceneParser:
    
    """A class to load map files into Panda3D."""
    
    def load(self, file_path):
        """Load the scene from an xml file."""
        self.nodes = {}
        self.connections = {}
        
        tree = et.parse(file_path)
        root_elem = tree.find('.//Component[@type="SceneRoot"]')
        self.load_component(root_elem, None)
            
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
        wrprCls = get_base().node_manager.GetWrapperByName(elem.get('type'))
        if wrprCls is not None:
            
            args = self.get_create_kwargs(wrprCls, elem)
            if 'path' in elem.attrib:
                args['parent'] = pComp
                args['path'] = elem.attrib['path']
            
            # Create the node and load it`s properties.
            wrpr = wrprCls.create(**args)
            if pComp is not None:
                try:
                    wrpr.parent = pComp
                except:
                    print(wrpr, wrpr.parent, pComp)
                    raise

            wrpr.id = elem.get('id')
            self.nodes[wrpr.id] = wrpr.data
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
                self.connections[wrpr] = cnctnDict
            
            # Recurse through hierarchy.
            for cElem in elem.findall('Component'):
                self.load_component(cElem, wrpr)
            
    def load_properties(self, comp, elem):
        
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

        for key, value_str in propDict.items():
            attr = comp.attributes[key]
            value = unserialise(value_str, attr.type)
            try:
                attr.set(value)
            except Exception as e:

                # TODO: Marshall properties first then remove those used in the
                # constructor so we don't try setting things like model path
                # here.
                print(e)
                logger.warning(f'Failed to set attribute: {attr.name}')
        
    def load_connections(self):
        for comp, connections in self.connections.items():
            for name, comp_ids in connections.items():
                for comp_id in comp_ids:
                    comp.attributes[name].connect(self.nodes[comp_id])
