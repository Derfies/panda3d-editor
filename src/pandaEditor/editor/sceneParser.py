import xml.etree.ElementTree as et

import game
from utils import indent


class SceneParser(game.SceneParser):
    
    def Save(self, scene, filePath):
        """Save the scene out to an xml file."""
        rootElem = et.Element('Scene')
        wrpr = base.game.nodeMgr.Wrap(scene)
        self.SaveComponent(wrpr, rootElem)
        
        # Wrap with an element tree and write to file.
        tree = et.ElementTree(rootElem)
        indent(tree.getroot())
        tree.write(filePath)
    
    def SaveComponent(self, wrpr, pElem):
        """Serialise a component to an xml element."""
        elem = pElem
        if wrpr.IsSaveable():
            
            # Write out component header data, then properties and 
            # connections.
            elem = et.SubElement(pElem, 'Component')
            for pName, pVal in wrpr.GetAttrib().items():
                elem.set(pName, pVal)
            self.SaveProperties(wrpr, elem)
            self.SaveConnections(wrpr, elem)
        
        # Write out addons.
        for cWrpr in wrpr.GetAddons():
            self.SaveComponent(cWrpr, elem)
        
        # Recurse through hierarchy.
        for cWrpr in wrpr.GetChildren():
            self.SaveComponent(cWrpr, elem)
                
    def SaveProperties(self, wrpr, elem):
        """
        Get a dictionary representing all the properties for the component
        then serialise it.
        """
        # Get a dictionary with all default values.
        defPropDict = wrpr.__class__.GetDefaultPropertyData()
        
        propDict = wrpr.GetPropertyData()
        for pName, pVal in propDict.items():
            if not type(pVal) == dict:
                
                # Compare the value to the default - serialise if they are
                # different.
                if pName in defPropDict and pVal == defPropDict[pName]:
                    continue
                
                elem.append(self.SaveItem(pName, pVal))
            else:
                subElem = et.SubElement(elem, 'Item')
                subElem.set('name', pName)
                for key, val in pVal.items():
                    subElem.append(self.SaveItem(key, val))
                
    def SaveItem(self, name, value):
        elem = et.Element('Item')
        elem.set('name', name)
        elem.set('value', value)
        return elem
                
    def SaveConnections(self, wrpr, elem):
        cnctnDict = wrpr.GetConnectionData()
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
