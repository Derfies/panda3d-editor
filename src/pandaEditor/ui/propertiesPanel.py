import logging

import wx

from wxExtra import wxpg
from pubsub import pub
import panda3d.core as pm
from panda3d.core import Filename
from pandaEditor import commands as cmds
from . import customProperties as custProps


logger = logging.getLogger(__name__)


ATTRIBUTE_TAG = 'attr'


class PropertyGrid(wxpg.PropertyGrid):
    """
    Unfortunately I've had to override some of the basic methods of the
    property grid in order to overcome what seems like an odd limitation /
    feature. When calling GetProperty() the grid sends back the base class
    PGProperty, not the actual class that was used when we initially called
    Append(). This seems odd to me as then none of the overridden methods used
    in custom properties will work...
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._propsByName = {}
        self._propsByLabel = {}
        self._propsByLongLabel = {}
    
    def Append(self, prop, *args, **kwargs):
        
        # Do not allow properties with '|' in the label as we use this as a
        # delimiter
        if '|' in prop.GetLabel():
            msg = ('Cannot use property labels containing the pipe (\'|\')' +
                    'character')
            raise AttributeError(msg)
        
        # Add the property
        wxpg.PropertyGrid.Append(self, prop, *args, **kwargs)
        
        # Store the property again in our dicts by name and label
        self._propsByName[prop.GetName()] = prop
        self._propsByLabel[prop.GetLabel()] = prop
        
        # Store the property plus all its children in the long label dict
        allProps = self._propsByLongLabel
        allChildren = self.GetAllChildren(prop)
        #self._propsByLongLabel = dict(allProps.items() + allChildren.items())
        
        def Rec(prop, res):
            res.append(prop)
            for cProp in prop.GetChildren():
                Rec(cProp, res)
        
        cProps = []
        Rec(prop, cProps)
        
        allProps = self._propsByLongLabel
        allChildren = {}
        for cProp in cProps:
            allChildren[self.GetPropertyLongLabel(cProp)] = cProp
        self._propsByLongLabel = {**allProps, **allChildren}
        
    def Clear(self):
        
        # Empty property dicts before using default clear method
        self._propsByName = {}
        self._propsByLabel = {}
        self._propsByLongLabel = {}
        
        wxpg.PropertyGrid.Clear(self)
        
    def GetPropertyByName(self, name):
        
        # Return value from the property dict
        if name in self._propsByName:
            return self._propsByName[name]
        
        return None
        
    def GetPropertyByLabel(self, label):
        
        # Return value from the property dict
        if label in self._propsByLabel:
            return self._propsByLabel[label]
        
        return None
    
    def GetPropertyByLongLabel(self, longLbl):
        """
        Return the property from the property dict matching the indicated
        long label.
        """
        if longLbl in self._propsByLongLabel:
            return self._propsByLongLabel[longLbl]
        
        return None
    
    def GetPropertyLongLabel(self, prop):
        """
        Return the property's long label. Do this by iterating to the top of
        the hierarchy and joining each parent's label with a pipe character 
        until there are no more parents.
        """
        elem = []
        
        while True:
            if prop.GetParent() is None:
                break
            else:
                elem.insert(0, prop.GetLabel())
                prop = prop.GetParent()
            
        return '|'.join(elem)
            
    
    def GetAllChildren(self, prop, parentLbl=None):
        """
        Return all decendant properties of the indicated property.
        """
        result = {}
        
        # Use property parent label if None is supplied
        if parentLbl is None:
            parentLbl = prop.GetParent().GetLabel()
        
        # Get the long label for this property
        lblElems = []
        if parentLbl:
            lblElems.append(parentLbl)
        lblElems.append(prop.GetLabel())
        longLbl = '|'.join(lblElems)
        
        # Add the property to the dictionary
        result[longLbl] = prop
        
        # Recurse down hierarchy
        for i in range(prop.GetCount()):
            result = {**result, **self.GetAllChildren(prop.Item(i), longLbl)}
        
        return result

    def GetProperties(self):
        
        # Return values of the property dict
        return self._propsByName.values()
    
    def GetPropertiesDictionary(self):
        """
        Return a flat dictionary containing all properties including all their
        decendants.
        """
        props = {}
        
        for propLabel, prop in self._propsByLabel.items():
            childs = self.GetAllChildren(prop)
            props = {**props, **childs}
        
        return props
    
    def Enable(self, value):
        """
        Overridden from wxpg.PropertyGrid. A disabled property grid doesn't
        seem to change in its appearance. Grey out all properties to give a
        nice visual indication of the state of the panel.
        """
        wxpg.PropertyGrid.Enable(self, value)
        
        # Remove the selection if we are disabling the panel
        if not value:
            self.SetSelection([])
        
        # Grey out all properties if we are disabling the panel
        for property in self.GetProperties():
            if value:
                self.SetPropertyColourToDefault(property)
            else:
                self.SetPropertyTextColour(property, wx.Colour(150, 150, 150))
                
    def OnChildFocus(self, evt):
        """
        Overriden to stop the property grid scrolling to the child which just
        received focus.
        """
        pass
    

class PropertiesPanel(wx.Panel):
    
    def __init__(self, base, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.base = base
        self.propExps = {}
        self.refocus = False
        
        # Define how each type of value should be edited
        self.propMap = {
            None:wxpg.PropertyCategory,
            pm.Vec2:custProps.Float2Property,
            pm.Vec3:custProps.Float3Property,
            pm.Vec4:custProps.Float4Property,
            pm.Point2:custProps.Point2Property,
            pm.Point3:custProps.Point3Property,
            pm.Point4:custProps.Point4Property,
            pm.NodePath:custProps.NodePathProperty,
            int:wxpg.IntProperty,
            str:wxpg.StringProperty,
            bool:wxpg.BoolProperty,
            float:wxpg.FloatProperty,
            Filename:custProps.FilePathProperty,
            dict:custProps.DictProperty
        }
        
        # Bind publisher events
        pub.subscribe(self.OnUpdate, 'Update')
        pub.subscribe(self.OnUpdate, 'UpdateSelection')
        pub.subscribe(self.OnSelectionModified, 'SelectionModified')
        
        # Build property grid
        self.pg = PropertyGrid(self)
        
        # Bind property grid events
        self.pg.Bind(wxpg.EVT_PG_CHANGED, self.OnPgChanged)
        
        # Build sizers
        self.bs1 = wx.BoxSizer(wx.VERTICAL)
        self.bs1.Add(self.pg, 1, wx.EXPAND)
        self.SetSizer(self.bs1)
        
    def BuildPropertyGrid(self, wrprs):
        """
        Build the properties for the grid based on the contents of nps.
        """
        self.pg.Clear()
        
        # Bail if there are no selected NodePaths.
        if not wrprs:
            return
        
        self.propAttrMap = {}
                        
        # Build all properties from attributes.
        comps = self.base.selection.comps
        wrprCls = base.node_manager.get_common_wrapper(comps)
        wrprs = [wrprCls(comp) for comp in comps]
        for i, attr in enumerate(wrprs[0].GetAttributes(addons=True)):
            
            # Find the correct property to display this attribute
            if attr.type in self.propMap and attr.getFn is not None:
                propCls = self.propMap[attr.type]
                if attr.type is not None:
                    prop = propCls(attr.label, '', attr.Get())
                    if attr.setFn is None:
                        prop.Enable(False)
                else:
                    prop = propCls(attr.label)
            elif hasattr(attr, 'cnnctn'):
                val = attr.Get()
                try:
                    objIter = iter(val)
                    prop = custProps.ConnectionListProperty(attr.label, '', attr.Get())
                except TypeError:
                    prop = custProps.ConnectionProperty(attr.label, '', attr.Get())
            else:
                continue
            
            if hasattr(attr, 'parent') and attr.parent not in self.propAttrMap and attr.parent is not None:
                pProp = wxpg.PropertyCategory(attr.parent)
                self.propAttrMap[attr.parent] = pProp
                self.pg.Append(pProp)
            
            allAttrs = [wrpr.GetAttributes(addons=True)[i] for wrpr in wrprs]
            prop.SetAttribute(ATTRIBUTE_TAG, allAttrs)
            self.propAttrMap[attr.label] = prop
                
            # Append to property grid or the last property if it is a 
            # child.
            if hasattr(attr, 'parent') and attr.parent in self.propAttrMap:
                self.propAttrMap[attr.parent].AddPrivateChild(prop)
            else:
                self.pg.Append(prop)
                            
    def OnPgChanged(self, evt):
        """
        Set the node path or node's property using the value the user entered
        into the grid.
        """
        # Should probably never get here...
        comps = self.base.selection.comps
        if not comps:
            return
        
        self.refocus = True
        
        # Get the node property from the property and set it.
        prop = evt.GetProperty()
        attrs = prop.GetAttribute(ATTRIBUTE_TAG)
        if not hasattr(attrs[0], 'cnnctn'):
            cmds.SetAttribute(comps, attrs, prop.GetValue())
        else:
            cmds.SetConnections(prop.GetValue(), attrs)
        
    def OnUpdate(self, comps=None):
        self.pg.Freeze()
        
        # Get the scroll position.
        x, y = self.pg.GetViewStart()
        
        # Get property expanded states and which property was focused.
        allProps = self.pg.GetPropertiesDictionary()
        for propLongLbl, prop in allProps.items():
            self.propExps[propLongLbl] = prop.IsExpanded()
            
        focusProp = self.pg.GetFocusedProperty()
        if focusProp is not None:
            focusPropLbl = self.pg.GetPropertyLongLabel(focusProp)
            focusIndex = self.pg.GetFocusedPropertyControl()
        
        # Clear and rebuild property grid
        self.BuildPropertyGrid(base.selection.wrprs)
        
        # Set all property expanded states back.
        for propLongLbl, expanded in self.propExps.items():
            prop = self.pg.GetPropertyByLongLabel(propLongLbl)
            if prop is not None:
                prop.SetExpanded(expanded)
        
        # Set the focused property back.
        if self.refocus and focusProp is not None:
            focusProp = self.pg.GetPropertyByLongLabel(focusPropLbl)
            if focusProp is not None:
                focusProp.SetFocus(focusIndex)
            else:
                logger.info('Missed focus')
        
        # Set the scroll position back.
        self.pg.Scroll(x, y)
        
        self.pg.Thaw()
        
        self.refocus = False
        
    def OnSelectionModified(self, comps):
        """
        Update the position, rotation and scale properties during the 
        transform operation.
        """
        wrpr = base.selection.wrprs[0]
        labelFnDict = {
            'Position':wrpr.data.getPos,
            'Rotation':wrpr.data.getHpr,
            'Scale':wrpr.data.getScale
        }
        
        # Set the value of each property to the result returned from calling
        # the function.
        for label, fn in labelFnDict.items():
            prop = self.pg.GetPropertyByLabel(label)
            if prop is not None:
                prop.SetValue(fn())
