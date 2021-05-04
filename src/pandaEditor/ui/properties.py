import copy

import wx
import panda3d.core as pc

import wx.propgrid as wxpg
from game.nodes.base import Base
from wxExtra.propertyGrid import PropertyGridEvent


class DataWrapper:

    def __init__(self, data):
        self.data = data


class DropItemMixin:

    def drag_drop_validate(self, x, y, data):
        return False

    def on_drop(self, x, y, data):
        raise NotImplementedError('N  drag drop handler')

    def post_changed_event(self):
        event = PropertyGridEvent(wxpg.EVT_PG_CHANGED.typeId)
        event.SetProperty(self)

        # Call after otherwise we crash!
        fn = lambda: self.GetGrid().GetEventHandler().ProcessEvent(event)
        wx.CallAfter(fn)


class BaseComponentProperty(DropItemMixin, wxpg.PGProperty):

    value_type = None
    components = []

    def __init__(self, label, name, value):
        super().__init__(label, name)
        self.SetValue(DataWrapper(list(value)))
        for i, comp in enumerate(self.components):
            self.AddPrivateChild(wxpg.FloatProperty(
                comp,
                value=self.m_value.data[i])
            )

    def RefreshChildren(self):
        try:
            for i, elem in enumerate(self.m_value.data):
                self.Item(i).SetValue(elem)
        except Exception as e:
            print('Fouled up refresh children:', self.GetName())
            raise

    def ChildChanged(self, value, child_index, child_value):
        value.data[child_index] = child_value
        return value

    def GetValue(self):
        return self.value_type(*self.m_value.data)


class Point2Property(BaseComponentProperty):

    value_type = pc.LPoint2f
    components = ['X', 'Y']


class Point3Property(BaseComponentProperty):

    value_type = pc.LPoint3f
    components = ['X', 'Y', 'Z']


class Point4Property(BaseComponentProperty):

    value_type = pc.LPoint4f
    components = ['X', 'Y', 'Z', 'W']


class Vec2Property(BaseComponentProperty):

    value_type = pc.LVecBase2f
    components = ['X', 'Y']


class Vec3Property(BaseComponentProperty):

    value_type = pc.LVecBase3f
    components = ['X', 'Y', 'Z']


class Vec4Property(BaseComponentProperty):

    value_type = pc.LVecBase4f
    components = ['X', 'Y', 'Z', 'W']


class ConnectionProperty(DropItemMixin, wxpg.StringProperty):

    def __init__(self, label, name, value):
        super().__init__(label, name)
        self.SetValue(DataWrapper(value))

    def ValueToString(self, value, argFlags=0):
        return value.data.name_ if value.data is not None else ''

    def drag_drop_validate(self, x, y, data):
        if not len(data) == 1:
            return False
        comp = data[0]
        if not isinstance(comp, Base):
            return False
        prop_type = self.GetAttribute('prop_value_type')
        return comp.is_of_type(prop_type)

    def on_drop(self, x, y, data):
        self.SetValue(DataWrapper(data[0]))
        self.post_changed_event()

    def GetValue(self):
        return self.m_value.data


class ConnectionsProperty(DropItemMixin, wxpg.StringProperty):

    def __init__(self, label, name, value):
        super().__init__(label, name)
        self.SetValue(DataWrapper(value))

    def ValueToString(self, value, argFlags=0):
        return ', '.join([comp.name_ for comp in value.data])

    def drag_drop_validate(self, x, y, data):
        prop_type = self.GetAttribute('prop_value_type')
        return all([
            isinstance(comp, Base) and comp.is_of_type(prop_type)
            for comp in data
        ])

    def on_drop(self, x, y, data):
        targets = self.GetValue()[:]
        targets.extend(data)
        self.SetValue(DataWrapper(targets))
        self.post_changed_event()

    def GetValue(self):
        return self.m_value.data


class ConnectionPropertyEditor(wxpg.PGEditor):

    def CreateControls(self, propgrid, property, pos, size):
        ctrl = wx.ListBox(
            propgrid.GetPanel(),
            wx.ID_ANY,
            pos=pos,
            size=wx.Size(size.x, -1),
            style=wx.BORDER_NONE
        )
        value = property.GetValue()
        if value is not None:
            ctrl.Append(value.name_)
        ctrl.Layout()
        return wxpg.PGWindowList(ctrl)

    def UpdateControl(self, property, ctrl):
        print('need to update')

    def OnEvent(self, propgrid, property, ctrl, evt):
        evt_type = evt.GetEventType()
        if (
            evt_type == wx.wxEVT_KEY_UP and
            evt.GetKeyCode() in (wx.WXK_DELETE, wx.WXK_BACK)
        ):
            property.SetValue(DataWrapper(None))
            property.post_changed_event()
            return True
        return False


class ConnectionsPropertyEditor(wxpg.PGEditor):

    def CreateControls(self, propgrid, property, pos, size):
        ctrl = wx.ListBox(
            propgrid.GetPanel(),
            wx.ID_ANY,
            pos=pos,
            size=wx.Size(size.x, -1),
            style=wx.BORDER_NONE | wx.LB_MULTIPLE
        )
        for comp in property.GetValue():
            ctrl.Append(comp.name_)
        ctrl.Layout()
        return wxpg.PGWindowList(ctrl)

    def UpdateControl(self, property, ctrl):
        print('need to update')

    def OnEvent(self, propgrid, property, ctrl, evt):
        evt_type = evt.GetEventType()
        if (
            evt_type == wx.wxEVT_KEY_UP and
            evt.GetKeyCode() in (wx.WXK_DELETE, wx.WXK_BACK)
        ):
            targets = property.GetValue()[:]
            for index in reversed(ctrl.GetSelections()):
                del targets[index]
            property.SetValue(DataWrapper(targets))
            property.post_changed_event()
            return True
        return False
