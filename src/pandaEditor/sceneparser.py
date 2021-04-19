import xml.etree.ElementTree as et
from direct.showbase.PythonUtil import getBase as get_base

from game.sceneparser import SceneParser as GameSceneParser
from utils import indent


class SceneParser(GameSceneParser):
    
    def save(self, scene, file_path):
        """Save the scene out to an xml file."""
        rootElem = et.Element('Scene')
        comp = get_base().node_manager.wrap(scene)
        self.save_component(comp, rootElem)
        
        # Wrap with an element tree and write to file.
        tree = et.ElementTree(rootElem)
        indent(tree.getroot())
        tree.write(file_path)
    
    def save_component(self, wrpr, pElem):
        """Serialise a component to an xml element."""
        elem = pElem
        if wrpr.savable:
            
            # Write out component header data, then properties and 
            # connections.
            elem = et.SubElement(pElem, 'Component')
            for pName, pVal in wrpr.get_attrib().items():
                elem.set(pName, pVal)
            self.save_properties(wrpr, elem)
            self.save_connections(wrpr, elem)
        
        # Recurse through hierarchy.
        for child in wrpr.children:
            self.save_component(child, elem)
                
    def save_properties(self, wrpr, elem):
        """
        Get a dictionary representing all the properties for the component
        then serialise it.
        """
        # Get a dictionary with all default values.
        defPropDict = wrpr.__class__.get_default_property_data()
        
        propDict = wrpr.get_property_data()
        for pName, pVal in propDict.items():
            if not type(pVal) == dict:
                
                # Compare the value to the default - serialise if they are
                # different.
                if pName in defPropDict and pVal == defPropDict[pName]:
                    continue
                
                elem.append(self.save_item(pName, pVal))
            else:
                subElem = et.SubElement(elem, 'Item')
                subElem.set('name', pNpame)
                for key, val in pVal.items():
                    subElem.append(self.save_item(key, val))
                
    def save_item(self, name, value):
        return et.Element('Item', {
            'name': name,
            'value': value,
        })
                
    def save_connections(self, wrpr, elem):
        cnctnDict = wrpr.get_connection_data()
        if not cnctnDict:
            return
        
        cnctnsElem = et.Element('Connections')
        for key, vals in cnctnDict.items():
            print('save:', key, vals)
            for val in vals:
                cnctnElem = et.SubElement(cnctnsElem, 'Connection')
                cnctnElem.set('type', key)
                cnctnElem.set('value', val)
                
        # Append the connections element only if it isn't empty.
        if list(cnctnsElem):
            elem.append(cnctnsElem)
