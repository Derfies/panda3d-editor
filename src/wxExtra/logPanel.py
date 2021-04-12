import logging

import wx


class LogPanel(wx.Panel):
    
    """
    Simple wxPanel containing a text control which will display the root
    logger's stream.

    """

    class CustomConsoleHandler(logging.StreamHandler):

        def __init__(self, text_ctrl, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.text_ctrl = text_ctrl

        def emit(self, record):
            msg = self.format(record)
            self.text_ctrl.WriteText(msg + '\n')
            self.flush()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Build log text control.
        style = wx.TE_MULTILINE | wx.TE_RICH2 | wx.NO_BORDER | wx.TE_READONLY
        text_ctrl = wx.TextCtrl(self, style=style)

        # Set up another logging stream that prints to the text control. Use
        # the default handler's formatter.
        root_log = logging.getLogger()
        handler = self.CustomConsoleHandler(text_ctrl)
        handler.formatter = root_log.handlers[0].formatter
        root_log.addHandler(handler)
        
        # Build sizers.
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_ctrl, 1, wx.EXPAND)
        self.SetSizer(sizer)
