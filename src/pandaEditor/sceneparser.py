import collections
import logging

import xml.etree.ElementTree as et
from direct.showbase.PythonUtil import getBase as get_base

from p3d.commonUtils import serialise
from game.sceneparser import SceneParser as GameSceneParser
from utils import indent


logger = logging.getLogger(__name__)


class SceneParser(GameSceneParser):
    
    def save(self, obj, file_path):
        """Save the scene out to an xml file."""
        comp = get_base().node_manager.wrap(obj)
        relem = self.save_component(comp, None)
        
        # Wrap with an element tree and write to file.
        tree = et.ElementTree(relem)
        indent(tree.getroot())
        tree.write(file_path)
    
    def save_component(self, comp, pelem):
        """Serialise a component to an xml element."""
        elem = pelem
        if comp.savable:
            
            # Write out component header data, then properties and 
            # connections.
            elem = et.Element('Component')
            if pelem is not None:
                pelem.append(elem)
            for name, value in comp.get_attrib().items():
                elem.set(name, value)
            self.save_properties(comp, elem)
            self.save_connections(comp, elem)
        
        # Recurse through hierarchy.
        for child in comp.children:
            self.save_component(child, elem)

        return elem
                
    def save_properties(self, comp, elem):
        """
        Get a dictionary representing all the properties for the component
        then serialise it.
        """

        # TODO: Move to attributes property on comp class like connections,
        # below.
        for attr_name, attr in comp.__class__.attributes.items():
            if not attr.serialise:
                continue
            value = getattr(comp, attr_name)
            if value is None:
                logger.warning(f'Skipped serialising None value: {attr_name}')
                continue
            item_elem = et.SubElement(elem, 'Item')
            item_elem.set('name', attr_name)
            item_elem.set('value', serialise(value))
                
    def save_connections(self, comp, elem):

        conns_elem = et.Element('Connections')
        for name, values in comp.connections.items():
            if not comp.__class__.connections[name].many:
                values = [values]
            for value in values:
                conn_elem = et.SubElement(conns_elem, 'Connection')
                conn_elem.set('type', name)
                conn_elem.set('value', value.id)
                
        # Append the connections element only if it isn't empty.
        if list(conns_elem):
            elem.append(conns_elem)
