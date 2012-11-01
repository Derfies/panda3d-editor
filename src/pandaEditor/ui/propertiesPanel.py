import wx
from wxExtra import wxpg
from wx.lib.pubsub import Publisher as pub
import pandac.PandaModules as pm

from .. import commands as cmds
import customProperties as custProps


ATTRIBUTE_TAG = 'attr'


class PropertyGrid( wxpg.PropertyGrid ):
    
    """
    Unfortunately I've had to override some of the basic methods of the
    property grid in order to overcome what seems like an odd limitation /
    feature. When calling GetProperty() the grid sends back the base class
    PGProperty, not the actual class that was used when we initially called
    Append(). This seems odd to me as then none of the overridden methods used
    in custom properties will work...
    """
    
    def __init__( self, *args, **kwargs ):
        wxpg.PropertyGrid.__init__( self, *args, **kwargs )
        
        self._propsByName = {}
        self._propsByLabel = {}
        self._propsByLongLabel = {}
    
    def Append( self, prop ):
        
        # Do not allow properties with '|' in the label as we use this as a
        # delimiter
        if '|' in prop.GetLabel():
            msg = ( 'Cannot use property labels containing the pipe (\'|\')' +
                    'character' )
            raise AttributeError, msg
        
        # Add the property
        wxpg.PropertyGrid.Append( self, prop )
        
        # Store the property again in our dicts by name and label
        self._propsByName[prop.GetName()] = prop
        self._propsByLabel[prop.GetLabel()] = prop
        
        # Store the property plus all its children in the long label dict
        allProps = self._propsByLongLabel
        allChildren = self.GetAllChildren( prop )
        self._propsByLongLabel = dict( allProps.items() + allChildren.items() )
        
    def Clear( self ):
        
        # Empty property dicts before using default clear method
        self._propsByName = {}
        self._propsByLabel = {}
        self._propsByLongLabel = {}
        
        wxpg.PropertyGrid.Clear( self )
        
    def GetPropertyByName( self, name ):
        
        # Return value from the property dict
        if name in self._propsByName:
            return self._propsByName[name]
        
        return None
        
    def GetPropertyByLabel( self, label ):
        
        # Return value from the property dict
        if label in self._propsByLabel:
            return self._propsByLabel[label]
        
        return None
    
    def GetPropertyByLongLabel( self, longLbl ):
        """
        Return the property from the property dict matching the indicated
        long label.
        """
        if longLbl in self._propsByLongLabel:
            return self._propsByLongLabel[longLbl]
        
        return None
    
    def GetPropertyLongLabel( self, prop ):
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
                elem.insert( 0, prop.GetLabel() )
                prop = prop.GetParent()
            
        return '|'.join( elem )
            
    
    def GetAllChildren( self, prop, parentLbl=None ):
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
            lblElems.append( parentLbl )
        lblElems.append( prop.GetLabel() )
        longLbl = '|'.join( lblElems )
        
        # Add the property to the dictionary
        result[longLbl] = prop
        
        # Recurse down hierarchy
        for i in range( prop.GetCount() ):
            result = dict( result.items() + self.GetAllChildren( prop.Item( i ), longLbl ).items() )
        
        return result

    def GetProperties( self ):
        
        # Return values of the property dict
        return self._propsByName.values()
    
    def GetPropertiesDictionary( self ):
        props = {}
        
        # Include children if specified
        for propLabel, prop in self._propsByLabel.items():
            
            # Ignore property categories
            if prop.IsCategory():
                props[prop.GetLabel()] = prop
                continue
            
            childs = self.GetAllChildren( prop )
            props = dict( props.items() + childs.items() )
        
        # Return values of the property dict
        return props
    
    def Enable( self, value ):
        """
        Overridden from wxpg.PropertyGrid. A disabled property grid doesn't
        seem to change in its appearance. Grey out all properties to give a
        nice visual indication of the state of the panel.
        """
        wxpg.PropertyGrid.Enable( self, value )
        
        # Remove the selection if we are disabling the panel
        if not value:
            self.SetSelection( [] )
        
        # Grey out all properties if we are disabling the panel
        for property in self.GetProperties():
            if value:
                self.SetPropertyColourToDefault( property )
            else:
                self.SetPropertyTextColour( property, wx.Colour(150, 150, 150) )
    

class PropertiesPanel( wx.Panel ):
    
    def __init__( self, *args, **kwargs ):
        wx.Panel.__init__( self, *args, **kwargs )
        
        self.propExps = {}
        
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
            float:wxpg.FloatProperty
        }
        
        # Bind publisher events
        pub.subscribe( self.OnUpdate, 'Update' )
        pub.subscribe( self.OnUpdate, 'UpdateSelection' )
        pub.subscribe( self.OnSelectionModified, 'SelectionModified' )
        
        # Build property grid
        self.pg = PropertyGrid( self )
        
        # Bind property grid events
        self.pg.Bind( wxpg.EVT_PG_CHANGED, self.OnPgChanged )
        
        # Build sizers
        self.bs1 = wx.BoxSizer( wx.VERTICAL )
        self.bs1.Add( self.pg, 1, wx.EXPAND )
        self.SetSizer( self.bs1 )
        
    def BuildPropertyGrid( self ):
        """
        Build the properties for the grid based on the contents of nps.
        """
        self.pg.Clear()
        
        # For convenience
        nps = wx.GetApp().selection.nps
        if not nps:
            return
        
        def RecurseAttribute( attr, parent=None ):
            
            # Find the correct property to display this attribute
            if attr.type in self.propMap:
                prop = None
                if attr.e:
                    propCls = self.propMap[attr.type]
                    if attr.type is not None:
                        prop = propCls( attr.label, '', attr.Get( nps[0] ) )
                        prop.SetAttribute( ATTRIBUTE_TAG, attr )
                    else:
                        prop = propCls( attr.label )
                    nextP = prop
                else:
                    nextP = parent
                
                # Recurse through attribute children.
                for child in attr.children:
                    RecurseAttribute( child, nextP )
                    
                if prop is None:
                    return
                    
                # Append to property grid or the last property if it is a 
                # child.
                #if parent is None:
                self.pg.Append( prop )
                #else:
                #    parent.AddPrivateChild( prop )
                        
        # Build all properties from attributes.
        wrpr = base.game.nodeMgr.Wrap( nps[0] )
        if wrpr is not None:
            for attr in wrpr.GetAttributes():
                RecurseAttribute( attr )
                            
    def OnPgChanged( self, evt ):
        """
        Set the node path or node's property using the value the user entered
        into the grid.
        """
        # Should probably never get here...
        nps = wx.GetApp().selection.nps
        if not nps:
            return
        
        # Get the node property from the property and set it.
        prop = evt.GetProperty()
        attr = prop.GetAttribute( ATTRIBUTE_TAG )
        
        cmds.SetAttribute( nps, attr, prop.GetValue() )
        
    def OnUpdate( self, msg ):
        self.pg.Freeze()
        
        # Get property expanded states
        allProps = self.pg.GetPropertiesDictionary()
        for propLongLbl, prop in allProps.items():
            self.propExps[propLongLbl] = prop.IsExpanded()
        
        # Clear and rebuild property grid
        self.BuildPropertyGrid()
        
        # Set expanded states back
        for propLongLbl, expanded in self.propExps.items():
            prop = self.pg.GetPropertyByLongLabel( propLongLbl )
            if prop is not None:
                prop.SetExpanded( expanded )
        
        self.pg.Thaw()
        
    def OnSelectionModified( self, msg ):
        """
        Update the position, rotation and scale properties during the 
        transform operation.
        """
        np = msg.data[0]
        labelFnDict = {
            'Position':np.getPos,
            'Rotation':np.getHpr,
            'Scale':np.getScale
        }
        
        # Set the value of each property to the result returned from calling
        # the function.
        for label, fn in labelFnDict.items():
            prop = self.pg.GetPropertyByLabel( label )
            if prop is not None:
                prop.SetValue( fn() )