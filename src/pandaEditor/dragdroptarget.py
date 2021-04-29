import pickle

import wx

from direct.showbase.PythonUtil import getBase as get_base


class DragDropTarget(wx.DropTarget):

    def __init__(self, validate_fn, drop_fn):
        super().__init__()

        self.validate_fn = validate_fn
        self.drop_fn = drop_fn
        do = wx.CustomDataObject('data')
        self.SetDataObject(do)

    def OnDragOver(self, x, y, d):
        data = get_base().drag_drop_manager.data
        return d if self.validate_fn(x, y, data) else wx.DragNone

    def OnData(self, x, y, d):
        if not self.GetData():
            return
        data_obj = self.GetDataObject()
        data = data_obj.GetData()
        self.drop_fn(x, y, pickle.loads(data))
        return d
