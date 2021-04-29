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
        pass

    def post_changed_event(self):
        event = PropertyGridEvent(wxpg.EVT_PG_CHANGED.typeId)
        event.SetProperty(self)

        # Call after otherwise we crash!
        # fn = lambda: self.GetGrid().GetEventHandler().ProcessEvent(event)
        # wx.CallAfter(fn)
        self.GetGrid().GetEventHandler().ProcessEvent(event)

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

    

# class Float3Property(wxpg.BaseProperty):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self._count = 3
#         self._cast = pm.Vec3 # HAXXOR
#
#     def BuildControl(self, parent):
#         bs = wx.BoxSizer(wx.HORIZONTAL)
#         for i in range(self._count):
#             ctrl = wx.TextCtrl(
#                 parent,
#                 i,
#                 style=wx.TE_PROCESS_ENTER,
#                 validator=wxpg.FloatValidator()
#            )
#             self.AppendControl(ctrl)
#             bs.Add(ctrl, 1, wx.EXPAND)
#         self.SetValue(self._value)
#         return bs
#
#     def SetValue(self, val):
#         wxpg.BaseProperty.SetValue(self, val)
#
#         for i, ctrl in enumerate(self.GetControls()):
#             rndVal = round(val[i], 3)
#             ctrl.SetValue(str(rndVal))
#
#     def SetValueFromEvent(self, evt):
#         self._value = self._cast(self._value)
#         ctrl = evt.GetEventObject()
#         index = ctrl.GetId()
#         try:
#             val = float(ctrl.GetValue())
#         except ValueError:
#             val = 0
#         self._value[index] = val
#
#
# class Float2Property(Float3Property):
#
#     def __init__(self, *args, **kwargs):
#         Float3Property.__init__(self, *args, **kwargs)
#
#         self._count = 2
#         self._cast = pm.Vec2
#
#
# class Float4Property(Float3Property):
#
#     def __init__(self, *args, **kwargs):
#         Float3Property.__init__(self, *args, **kwargs)
#
#         self._count = 4
#         self._cast = pm.Vec4
#
#
# class Point2Property(Float3Property):
#
#     def __init__(self, *args, **kwargs):
#         Float3Property.__init__(self, *args, **kwargs)
#
#         self._count = 2
#         self._cast = pm.Point2
#
#
# class Point3Property(Float3Property):
#
#     def __init__(self, *args, **kwargs):
#         Float3Property.__init__(self, *args, **kwargs)
#
#         self._count = 3
#         self._cast = pm.Point3
#
#
# class Point4Property(Float3Property):
#
#     def __init__(self, *args, **kwargs):
#         Float3Property.__init__(self, *args, **kwargs)
#
#         self._count = 4
#         self._cast = pm.Point4
#
#
# class FilePathProperty(wxpg.StringProperty):
#
#     def SetValueFromEvent(self, evt):
#         ctrl = evt.GetEventObject()
#         val = ctrl.GetValue()
#         self.SetValue(Filename.fromOsSpecific(val))
#
#     def BuildControl(self, *args, **kwargs):
#         ctrl = wxpg.StringProperty.BuildControl(self, *args, **kwargs)
#         dt = CompositeDropTarget(['filePath'], self.OnDropItem, self.drag_drop_validate)
#         ctrl.SetDropTarget(dt)
#         return ctrl
#
#     def OnDropItem(self, arg):
#         self.SetValue(arg)
#         self.PostChangedEvent()
#
#     def drag_drop_validate(self, *args):
#         return True
#
#
# class NodePathProperty(wxpg.StringProperty):
#
#     def BuildControl(self, parent):
#         np = self.GetValue()
#         text = ''
#         if np is not None:
#             text = np.getName()
#
#         ctrl = wx.TextCtrl(parent, -1, value=text)
#         ctrl.Bind(wx.EVT_TEXT, self.OnChanged)
#
#         dt = CompositeDropTarget(['nodePath', 'filePath'],
#                                   self.OnDropItem,
#                                   self.drag_drop_validate)
#         ctrl.SetDropTarget(dt)
#
#         return ctrl
#
#     def drag_drop_validate(self, x, y):
#         return True
#
#     def OnDropItem(self, arg):
#         np = wx.GetApp().frame.pnlSceneGraph.drag_comps[0]
#         self.SetValue(np)
#
#         self.PostChangedEvent()
#
#
# class ConnectionBaseProperty(wxpg.BaseProperty):
#
#     def BuildControl(self, parent, height):
#         ctrl = wx.ListBox(parent, -1, size=wx.Size(-1, height), style=wx.LB_EXTENDED)
#         ctrl.Enable(self.IsEnabled())
#         ctrl.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
#
#         dt = CompositeDropTarget(['nodePath'],
#                                   self.OnDropItem,
#                                   self.drag_drop_validate)
#         ctrl.SetDropTarget(dt)
#
#         return ctrl
#
#     def OnKeyUp(self, evt):
#         pass
#
#     def drag_drop_validate(self, x, y):
#         for comp in wx.GetApp().GetTopWindow().pnlSceneGraph.drag_comps:
#             prop_type = self.GetAttribute('prop_value_type')
#             if comp.is_of_type(prop_type):
#                 return True
#         return False
#
#
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
        self.SetValue(DataWrapper(data))
        self.post_changed_event()


class ConnectionsPropertyEditor(wxpg.PGEditor):

    def CreateControls(self, propgrid, property, pos, size):
        ctrl = wx.ListBox(
            propgrid.GetPanel(),
            wx.ID_ANY,
            pos=pos,
            #size=size,
            size=wx.Size(size.x, -1),
            style=wx.BORDER_NONE
        )
        for comp in property.GetValue().data:
            print('comp:', comp)
            ctrl.Append(comp.name_)
        # for d in dir(ctrl):
        #     print(d)
        #         ctrl.Enable(self.IsEnabled())
        #         ctrl.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        ctrl.Layout()
        return wxpg.PGWindowList(ctrl)

    # def SetControlStringValue(self, property, ctrl, txt):
    #     print('here')
    #
    # def UpdateControl(self, property, ctrl):
    #     #ctrl.SetValue(property.GetDisplayedString())
    #
    #     # if comp is not None:
    #     #     wrpr = get_base().node_manager.wrap(comp)
    #     #     ctrl.Append(wrpr.name_)
    #     #     ctrl.SetClientData(0, wrpr.data)
    #     print('->', property, ctrl)
    #
    # def DrawValue(self, dc, rect, property, text):
    #     if not property.IsValueUnspecified():
    #         dc.DrawText(property.GetDisplayedString(), rect.x+5, rect.y)

    def OnEvent(self, propgrid, property, ctrl, event):
        #if not ctrl:
        return False


#
#     def BuildControl(self, parent):
#         height = parent.GetSize()[1]
#         ctrl = ConnectionBaseProperty.BuildControl(self, parent, height)
#
#         comp = self.GetValue()
#         if comp is not None:
#             wrpr = get_base().node_manager.wrap(comp)
#             ctrl.Append(wrpr.name_)
#             ctrl.SetClientData(0, wrpr.data)
#
#         return ctrl
#
#     def OnKeyUp(self, evt):
#         if evt.GetKeyCode() not in [wx.WXK_DELETE, wx.WXK_BACK]:
#             return
#
#         self.SetValue(None)
#         self.PostChangedEvent()
#
#     def OnDropItem(self, arg):
#         val = wx.GetApp().GetTopWindow().pnlSceneGraph.drag_comps[0]
#         self.SetValue(val)
#         self.PostChangedEvent()
#
#
# class ConnectionListProperty(ConnectionBaseProperty):
#
#     def BuildControl(self, parent):
#         ctrl = ConnectionBaseProperty.BuildControl(self, parent, -1)
#         comps = self.GetValue() or []
#         for comp in comps:
#             ctrl.Append(comp.name_, comp)
#         return ctrl
#
#     def OnKeyUp(self, evt):
#         """
#         Remove those components that were selected in the list box from this
#         property's value.
#         """
#         if evt.GetKeyCode() not in [wx.WXK_DELETE, wx.WXK_BACK]:
#             return
#
#         lb = evt.GetEventObject()
#         delComps = [lb.GetClientData(index) for index in lb.GetSelections()]
#         oldComps = self.GetValue()
#         newComps = [comp for comp in oldComps if comp not in delComps]
#         self.SetValue(newComps)
#         self.PostChangedEvent()
#
#     def OnDropItem(self, arg):
#
#         import pickle
#
#         val = list(self.GetValue())
#         if val is None:
#             val = []
#         val.extend(wx.GetApp().GetTopWindow().pnlSceneGraph.drag_comps)
#         self.SetValue(val)
#         self.PostChangedEvent()
#
#
# class DictProperty(wxpg.BaseProperty):
#
#     def BuildControl(self, parent):
#         ctrl = CustomListCtrl(parent, -1, style=wx.LC_REPORT | wx.LC_EDIT_LABELS)
#         ctrl.InsertColumn(0, 'Name')
#         ctrl.InsertColumn(1, 'Value')
#         ctrl.Enable(self.IsEnabled())
#         ctrl.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
#         ctrl.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnListEndLabelEdit)
#
#         dt = CompositeDropTarget(['nodePath'],
#                                   self.OnDropItem,
#                                   self.drag_drop_validate)
#         ctrl.SetDropTarget(dt)
#
#         for key, val in self.GetValue().items():
#             ctrl.InsertStringItem(0, str(key))
#             ctrl.SetStringItem(0, 1, str(val))
#
#         return ctrl
#
#     def drag_drop_validate(self, x, y):
#         return True
#
#     def OnKeyUp(self, evt):
#         if evt.GetKeyCode() not in [wx.WXK_DELETE, wx.WXK_BACK]:
#             return
#
#         # Get the names of the items selected, then remove these keys from
#         # the dictionary.
#         ctrl = evt.GetEventObject()
#         keys = [item.GetText() for item in ctrl.GetAllItems()]
#         myDict = dict(self.GetValue())
#         for index in ctrl.GetSelections():
#             del myDict[keys[index]]
#
#         self.SetValue(myDict)
#         self.PostChangedEvent()
#
#     def OnDropItem(self, arg):
#         myDict = dict(self.GetValue())
#         key = os.path.split(arg)[-1].split('.')[0]
#         myDict[key] = arg
#         self.SetValue(myDict)
#         self.PostChangedEvent()
#
#     def OnListEndLabelEdit(self, evt):
#
#         item = evt.GetItem()
#         ctrl = evt.GetEventObject()
#         oldKey = ctrl.GetItem(item.GetId()).GetText()
#         newKey = item.GetText()
#
#         pDict = self.GetValue()
#         val = pDict.pop(oldKey)
#         pDict[newKey] = val
#         self.SetValue(pDict)
#         self.PostChangedEvent()
