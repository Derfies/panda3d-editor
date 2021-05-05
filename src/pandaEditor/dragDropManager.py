import logging

import wx


logger = logging.getLogger(__name__)


class DragDropManager:

    def start(self, ctrl, data):
        logging.info(f'Start drag drop: {data}')

        self.data = data
        do = wx.CustomDataObject('data')
        ds = wx.DropSource(ctrl)
        ds.SetData(do)
        ds.DoDragDrop(True)
