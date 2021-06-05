import panda3d.core as pc
import wx
from wx.lib.agw.floatspin import FloatSpin
from wx.lib.intctrl import IntCtrl

from pandaEditor.utils import camel_case_to_label
from wxExtra.propertyGrid import FloatValidator


class BaseCtrl(wx.Control):

    type_ = pc.Vec3

    def __init__(self, *args, **kwargs):
        values = kwargs.pop('value')
        super().__init__(*args, **kwargs)

        self._mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        self._text_ctrls = []
        for i in range(3):
            text_ctrl = wx.TextCtrl(
                self,
                wx.ID_ANY,
                str(values[i]),
                validator=FloatValidator(),
                style=wx.TE_PROCESS_ENTER,
            )
            text_ctrl.SetInitialSize(wx.Size(60, -1))
            self._text_ctrls.append(text_ctrl)
            self._mainsizer.Add(text_ctrl, 1)
        self.SetSizer(self._mainsizer)
        self._mainsizer.Layout()

    def GetValue(self):
        return self.type_(*[float(ctrl.GetValue()) for ctrl in self._text_ctrls])


class Vec3Ctrl(BaseCtrl):

    type_ = pc.Vec3


class Point3Ctrl(BaseCtrl):

    type_ = pc.Point3


class PropFloatSpin(FloatSpin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, digits=2, **kwargs)


PROPERTY_MAP = {
    int: IntCtrl,
    float: PropFloatSpin,
    str: wx.TextCtrl,
    pc.Point3: Point3Ctrl,
    pc.Vec3: Vec3Ctrl,
}


class CreateDialog(wx.Dialog):

    def __init__(self, text, default_values, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ctrls = {}

        static_text = wx.StaticText(self, -1, text)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(static_text, 0, wx.TOP | wx.LEFT | wx.RIGHT, 10)

        for name, value in default_values.items():
            value_type = type(value)
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            label = camel_case_to_label(name)
            hsizer.Add(wx.StaticText(self, -1, label), 1)
            ctrl_cls = PROPERTY_MAP[value_type]
            ctrl = ctrl_cls(self, -1, value=value)
            self.ctrls[name] = ctrl
            hsizer.Add(ctrl, 1)
            sizer.Add(hsizer, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)

        buttons = self.CreateSeparatedButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(buttons, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizerAndFit(sizer)

    def GetValues(self):
        return {
            name: ctrl.GetValue()
            for name, ctrl in self.ctrls.items()
        }

    def Validate(self):
        result = super().Validate()
        if result:
            self.EndModal(wx.ID_OK)
        return result
