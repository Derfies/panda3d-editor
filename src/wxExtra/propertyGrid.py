import string

import wx
import wx.lib.intctrl
import wx.lib.agw.floatspin as fs
import wx.lib.scrolledpanel as scrolled
from wx.lib.embeddedimage import PyEmbeddedImage
from wx.lib.newevent import NewEvent


expand = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAAZiS0dE"
    "AP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9oCBRUpC/sWEUMAAAA9"
    "SURBVDjLY2AY1uA/MYqYKDWEiVKXMFHqHSZKw4SJ0oAl1QBGSgxgpMQLjCQHIiMTBOPTjN9K"
    "JuJS4sADAOgbBxlBsfXrAAAAAElFTkSuQmCC"
    )

collapse = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAAZiS0dE"
    "AP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9oCBRMnAPbKmfcAAABB"
    "SURBVDjLY2AYBcMAMKJwmBj+//9HhCYmBob//yB6GbFI4jUEWTNWA6DgP9GuxqPwPyHNhAxA"
    "N4SR3ID+P8wTEgBwLg4FdgEHxgAAAABJRU5ErkJggg=="
    )
    

EvtIconClick, EVT_ICON_CLICK = NewEvent()
EvtIconToggle, EVT_ICON_TOGGLE = NewEvent()

wxEVT_PG_CHANGED = wx.NewEventType()
EVT_PG_CHANGED = wx.PyEventBinder(wxEVT_PG_CHANGED, 0)

wxEVT_PG_RIGHT_CLICK = wx.NewEventType()
EVT_PG_RIGHT_CLICK = wx.PyEventBinder(wxEVT_PG_RIGHT_CLICK, 0)


class FloatValidator(wx.Validator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return FloatValidator()

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()
        
        for x in val:
            if x not in string.digits:
                return False

        return True

    def OnChar(self, event):
        key = event.GetKeyCode()
        char = chr(key)
        
        okKeys = [
            wx.WXK_DELETE, 
            wx.WXK_NUMPAD_ENTER, 
            wx.WXK_RETURN, 
            wx.WXK_TAB,
            wx.WXK_NUMPAD_SUBTRACT,
            wx.WXK_SUBTRACT
        ]
        
        if key < wx.WXK_SPACE or key in okKeys or key > 255 or char == '-':
            event.Skip()
            return

        # Allow the key stroke if is is a number or if this is the first 
        # decimal point we have encountered.
        val = self.GetWindow().GetValue()
        if char in string.digits or (char == '.' and '.' not in val):
            event.Skip()
            return

        if not wx.Validator_IsSilent():
            wx.Bell()

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return
    

class PropertyGridEvent(wx.PyCommandEvent):
    
    def __init__(self, evtType):
        super().__init__(evtType)
        
        self._prop = None
        
    def GetProperty(self):
        return self._prop
    
    def SetProperty(self, prop):
        self._prop = prop
    

class BaseProperty(object):
    
    def __init__(self, label, name, value):
        self._label = label
        self._name = name
        self._value = value
        
        self._window = None
        self._grid = None
        self._parent = None
        self._enabled = True
        self._children = []
        self._attrs = {}
        self._ctrls = []
        
    def GetLabel(self):
        return self._label
    
    def GetName(self):
        return self._name
    
    def GetValue(self):
        return self._value
    
    def SetValue(self, value):
        self._value = value
        
    def GetGrid(self):
        return self._grid
    
    def SetGrid(self, grid):
        self._grid = grid
    
    def GetParent(self):
        return self._parent
    
    def SetParent(self, parent):
        self._parent = parent
        
    def IsEnabled(self):
        return self._enabled
    
    def Enable(self, val):
        self._enabled = val
        
    def GetCount(self):
        return len(self._children)
    
    def Item(self, index):
        return self._children[index]
    
    def GetChildren(self):
        return self._children
    
    def AddPrivateChild(self, child):
        self._children.append(child)
        
        win = self.GetWindow()
        if win is not None:
            self.GetGrid().Append(child, win)
    
    def GetAttribute(self, name):
        return self._attrs[name]
    
    def SetAttribute(self, name, value):
        self._attrs[name] = value
        
    def IsCategory(self):
        return False
    
    def IsExpanded(self):
        return self._window.IsExpanded()
    
    def SetExpanded(self, val):
        self._window.Expand(val)
        
    def GetWindow(self):
        return self._window
        
    def SetWindow(self, win):
        self._window = win
    
    def BuildControl(self, *args, **kwargs):
        return None
    
    def SetValueFromEvent(self, evt):
        ctrl = evt.GetEventObject()
        self.SetValue(ctrl.GetValue())
    
    def OnChanged(self, evt):
        self.SetValueFromEvent(evt)
        self.PostChangedEvent()
        
    def PostChangedEvent(self):
        
        # Call after otherwise we crash!
        evt = PropertyGridEvent(wxEVT_PG_CHANGED)
        evt.SetProperty(self)
        fn = lambda : self.GetGrid().GetEventHandler().ProcessEvent(evt)
        wx.CallAfter(fn)
        
    def SetFocus(self, index):
        index = max(0, index)
        if self._ctrls:
            wx.CallAfter(self._ctrls[index].SetFocus)
            
    def AppendControl(self, ctrl):
        ctrl.Enable(self.IsEnabled())
        if isinstance(ctrl, wx.TextCtrl):
            ctrl.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
            ctrl.Bind(wx.EVT_CHILD_FOCUS, self.OnChildFocus)
            ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnChanged)
        elif isinstance(ctrl, wx.CheckBox):
            ctrl.Bind(wx.EVT_CHECKBOX, self.OnChanged)
        self._ctrls.append(ctrl)
        
    def GetControls(self):
        return self._ctrls
        
    def OnKillFocus(self, evt):
        """
        Bind a control's wx.EVT_KILL_FOCUS event to this method so that the 
        control's value is updated if it loses focus after being changed. This
        will also dehighlight the field.
        """
        ctrl = evt.GetEventObject()
        if ctrl.IsModified():
            self.OnChanged(evt)
        else:
            ctrl.SetSelection(0, 0)
    
    def OnChildFocus(self, evt):
        """
        Bind a control's wx.EVT_CHILD_FOCUS event to this method so that the
        text is immediately highlighted when the user clicks inside the field.
        """
        def SetSelection(ctrl):
            try:
                ctrl.SetSelection(-1, -1)
            except:
                pass
            
        ctrl = evt.GetEventObject()
        self.GetGrid().SetFocusedProperty(self)
        self.GetGrid().SetFocusedPropertyControl(ctrl.GetId())
        wx.CallAfter(SetSelection, ctrl)
        

class PropertyCategory(BaseProperty):
    
    def __init__(self, label, **kwargs):
        BaseProperty.__init__(self, label, '', None, **kwargs)
        
    def IsCategory(self):
        return True
    

class BoolProperty(BaseProperty):
    
    def SetValue(self, val):
        BaseProperty.SetValue(self, val)
        
        ctrl = self.GetControls()[0]
        ctrl.SetValue(self.GetValue())
        
    def SetValueFromEvent(self, evt):
        self._value = evt.IsChecked()
        
    def BuildControl(self, parent):
        ctrl = wx.CheckBox(parent, -1, style=wx.ALIGN_RIGHT)
        #ctrl.SetValue(self.GetValue())
        self.AppendControl(ctrl)
        self.SetValue(self.GetValue())
        return ctrl
    

class IntProperty(BaseProperty):
        
    def BuildControl(self, parent):
        ctrl = wx.lib.intctrl.IntCtrl(parent, -1)
        ctrl.SetValue(self.GetValue())
        self.AppendControl(ctrl)
        return ctrl
        

class FloatProperty(BaseProperty):
        
    def BuildControl(self, parent):
        rndValue = round(self._value, 3)
        ctrl = wx.TextCtrl(
            parent,
            -1,
            style=wx.TE_PROCESS_ENTER,
            value=str(rndValue),
            validator=FloatValidator()
        )
        self.AppendControl(ctrl)
        return ctrl
    
    def SetValueFromEvent(self, evt):
        ctrl = evt.GetEventObject()
        try:
            val = float(ctrl.GetValue())
        except ValueError:
            val = 0
        self.SetValue(val)
    

class StringProperty(BaseProperty):
        
    def BuildControl(self, parent):
        ctrl = wx.TextCtrl(
            parent,
            -1,
            style=wx.TE_PROCESS_ENTER,
            value=str(self.GetValue()),
        )
        self.AppendControl(ctrl)
        return ctrl
            

class ToggleIcon(wx.Panel):
    def __init__(self, parent, id, bitmapTrue, bitmapFalse, pos=wx.DefaultPosition):
        if bitmapTrue.GetSize() !=bitmapFalse.GetSize():
            raise Exception('Bitmaps are different sizes!')
        size = bitmapTrue.GetSize()
        
        wx.Panel.__init__(self, parent, id, pos, size)

        self._bitmapTrue = bitmapTrue
        self._bitmapFalse = bitmapFalse
        self._disabled_bitmap = True

        self._hover = False
        self._state = False

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnButton)
    
    def SetState(self, flag=True):
        """Set the state of the toogle."""
        self._state = bool(flag)
        self.Refresh()

    def GetState(self):
        """Get the state of the toogle."""
        return self._state

    def Toggle(self):
        """Switch state"""
        self._state = not self._state
        self.Refresh()

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        if self.IsEnabled():
            if self._state is True:
                dc.DrawBitmap(self._bitmapTrue, 0, 0, True)
            else:
                dc.DrawBitmap(self._bitmapFalse, 0, 0, True)
        elif self._disabled_bitmap is not False:
            if self._state is True:
                dc.DrawBitmap(self._bitmapTrue, 0, 0, True)
            else:
                dc.DrawBitmap(self._bitmapFalse, 0, 0, True)

    def OnButton(self, evt):
        if self.IsEnabled():
            self.Toggle()
            evt = EvtIconToggle(state=self._state)
            self.ProcessEvent(evt)
    

class BasePanel(wx.Panel):
    
    def __init__(self, grid, prop, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        
        self.grid = grid
        self.prop = prop
        self._windows = []
        self._margin = 0
        
        # Build sizers
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        
    def AddWindow(self, window):
        self.sizer.Add(window, 0, wx.LEFT | wx.EXPAND, self._margin)
        self._windows.append(window)
        
    def GetWindows(self):
        return self._windows
    
    def ClearWindows(self):
        for win in self._windows:
            win.Destroy()
        self._windows = []
    

class CollapsiblePanel(BasePanel):
    
    def __init__(self, *args, **kwargs):
        BasePanel.__init__(self, *args, **kwargs)
        
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        
        self.hidden = False
        self._margin = 5
        
        # Add the label
        self.label = wx.StaticText(self, -1, self.prop.GetLabel())
        if self.prop.IsCategory():
            labelfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            labelfont.SetWeight(wx.BOLD)
            self.label.SetFont(labelfont)
        
        # Button and label go in seperate sizer
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2.PrependSpacer(16)
        self.sizer2.Add(self.label, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2, 1, wx.EXPAND)
        
        # Create the control
        ctrl = self.prop.BuildControl(self)
        if ctrl is not None:
            self.sizer2.Add(ctrl, 4, wx.RIGHT, 5)
        
        self.Collapse()
        
    def BuildButton(self):
        self.but = ToggleIcon(self, -1, collapse.GetBitmap(), expand.GetBitmap())
        self.but.SetBackgroundColour(self.GetBackgroundColour())
        self.but.Bind(EVT_ICON_TOGGLE, self.OnButton)
        self.sizer2.Prepend(self.but, 0, wx.ALIGN_CENTER, 0)
        
        # Remove the spacer now that there is a button
        self.sizer2.Remove(0)

    def AddWindow(self, window):
        BasePanel.AddWindow(self, window)
        window.Show(not self.hidden)
        
        # Add collapse button
        if not hasattr(self, 'but'):
            self.BuildButton()

    def SetBackgroundColour(self,colour):
        if hasattr(self, 'but'):
            self.but.SetBackgroundColour(colour)
        wx.Panel.SetBackgroundColour(self, colour)

    def SetLabelFont(self, font):
        """Set the label font."""
        self.label.SetFont(font)

    def Expand(self, flag=True):
        """Expand (or collapse) the panel, flag=True to expand"""
        for win in self._windows:
            win.Show(flag)
        self.hidden = not flag
        
        # Make sure to update the button to reflect the current state
        if hasattr(self, 'but'):
            self.but.SetState(not self.hidden)
        
        # Layout has changed, make sure to refresh the entire tree.
        self.grid.RecurseLayout(self.grid.panel)
        self.grid.FitInside()

    def Collapse(self):
        """Collapse the panel."""
        self.Expand(False)
        
    def IsExpanded(self):
        return not self.hidden

    def OnButton(self, evt):
        self.Expand(self.hidden)
    

class PropertyGrid(scrolled.ScrolledPanel):
    
    def __init__(self, *args, **kwargs):
        scrolled.ScrolledPanel. __init__(self, *args, **kwargs)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        
        self._props = []
        self.panel = BasePanel(self, BaseProperty('', '', None), self)
        self._currParent = self.panel
        self._focusProp = None
        
        # Build sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        
        self.SetAutoLayout(1)
        self.SetupScrolling()
        
    def Append(self, prop, parent=None):
        
        # Only parent categories to the top level.
        if type(prop) == PropertyCategory:
            self._currParent = self.panel
            
        # Default the parent to the currect parent.
        if parent is None:
            parent = self._currParent
        
        pnl = CollapsiblePanel(self, prop, parent)
        parent.AddWindow(pnl)
        prop.SetWindow(pnl)
        prop.SetGrid(self)
        prop.SetParent(parent.prop)
        self._props.append(prop)
        
        # Set current parent if the property was a category
        if type(prop) == PropertyCategory:
            self._currParent = pnl
            
    def RecurseLayout(self, ctrl=None):
        """
        Recurse down the hierarchy calling Layout and Refresh on each window
        to make sure it's the right size.
        """
        ctrl.Layout()
        ctrl.Refresh()
        for child in ctrl.GetChildren():
            self.RecurseLayout(child)
            
    def Clear(self):
        self.panel.DestroyChildren()
        
    def OnChildFocus(self, evt):
        """
        Overriden to stop the property grid scrolling to the child which just
        received focus.
        """
        pass
    
    def GetFocusedProperty(self):
        return self._focusProp
    
    def SetFocusedProperty(self, prop):
        self._focusProp = prop
        
    def GetFocusedPropertyControl(self):
        return self._focusPropIndex
        
    def SetFocusedPropertyControl(self, index):
        self._focusPropIndex = index
