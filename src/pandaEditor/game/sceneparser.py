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
        root = tree.find('.//Component[@type="SceneRoot"]')
        self.load_component(root, None)
        self.load_connections()

    def get_attributes(self, pelem, comp_cls):
        attrs = {}
        for elem in pelem.findall('Item'):
            name = elem.get('name')
            value_str = elem.get('value')
            value_type = comp_cls._declared_fields[name].type
            attrs[name] = unserialise(value_str, value_type)
        return attrs
            
    def load_component(self, elem, pcomp):
        comp_type = elem.get('type')
        comp_cls = get_base().node_manager.get_component_by_name(comp_type)
        if comp_cls is not None:

            # Collect attribute keys and values.
            attrs = self.get_attributes(elem, comp_cls)
            kwargs = {
                attr.name: attrs.pop(attr.name)
                for attr in comp_cls.create_attributes
            }

            # For sub-models edits we need to pull out the path for the
            # constructor.
            if 'path' in elem.attrib:
                kwargs['path'] = elem.attrib['path']
                kwargs['parent'] = pcomp
            
            # Create the node and load it`s properties.
            comp = comp_cls.create(**kwargs)
            if pcomp is not None:
                comp.parent = pcomp
            comp.id = elem.get('id')
            self.nodes[comp.id] = comp.data

            for name, value in attrs.items():
                comp.attributes[name].set(value)
            
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
                self.connections[comp] = cnctnDict
            
            # Recurse through hierarchy.
            for cElem in elem.findall('Component'):
                self.load_component(cElem, comp)
        
    def load_connections(self):
        for comp, connections in self.connections.items():
            for name, comp_ids in connections.items():
                for comp_id in comp_ids:
                    comp.attributes[name].connect(self.nodes[comp_id])
