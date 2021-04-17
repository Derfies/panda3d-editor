import xml.etree.ElementTree as et

from game.sceneparser import SceneParser
from utils import indent


class SceneParser(SceneParser):
    
    def save(self, scene, filePath):
        """Save the scene out to an xml file."""
        rootElem = et.Element('Scene')
        wrpr = base.node_manager.wrap(scene)
        self.save_component(wrpr, rootElem)
        
        # Wrap with an element tree and write to file.
        tree = et.ElementTree(rootElem)
        indent(tree.getroot())
        tree.write(filePath)
    
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
        
        # Write out addons.
        for cWrpr in wrpr.get_add_ons():
            self.save_component(cWrpr, elem)
        
        # Recurse through hierarchy.
        children = wrpr.get_children()
        for child in children:
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
                subElem.set('name', pName)
                for key, val in pVal.items():
                    subElem.append(self.save_item(key, val))
                
    def save_item(self, name, value):
        elem = et.Element('Item')
        elem.set('name', name)
        elem.set('value', value)
        return elem
                
    def save_connections(self, wrpr, elem):
        cnctnDict = wrpr.get_connection_data()
        if not cnctnDict:
            return
        
        cnctnsElem = et.Element('Connections')
        for key, vals in cnctnDict.items():
            for val in vals:
                cnctnElem = et.SubElement(cnctnsElem, 'Connection')
                cnctnElem.set('type', key)
                cnctnElem.set('value', val)
                
        # Append the connections element only if it isn't empty.
        if list(cnctnsElem):
            elem.append(cnctnsElem)
