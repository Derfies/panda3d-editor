import os

import wx
import wx.lib.agw.customtreectrl as ct
from p3d import wxPanda
from pubsub import pub

from wxExtra import DirTreeCtrl, utils as wxUtils
from direct.showbase.PythonUtil import getBase as get_base


class ResourcesPanel(wx.Panel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Bind project file events
        pub.subscribe(self.OnUpdate, 'projectFilesAdded')
        pub.subscribe(self.OnUpdate, 'projectFilesRemoved')

        # Build sizers
        self.bs1 = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.bs1)

    def Build(self, projDirPath):

        # Clear all widgets from the sizer
        self.bs1.Clear(True)
        if projDirPath is not None and os.path.isdir(projDirPath):

            # Build tree control and add it to the sizer
            style = (
                ct.TR_EDIT_LABELS |
                ct.TR_FULL_ROW_HIGHLIGHT |
                ct.TR_HAS_BUTTONS |
                ct.TR_MULTIPLE
            )
            self.dtc = DirTreeCtrl(self, -1, agwStyle=style)
            self.dtc.SetRootDir(projDirPath)
            self.dtc.Expand(self.dtc.GetRootItem())
            self.bs1.Add(self.dtc, 1, wx.EXPAND)

            self.dtc.Bind(wx.EVT_KEY_UP, wxPanda.OnKeyUp)
            self.dtc.Bind(wx.EVT_KEY_DOWN, wxPanda.OnKeyDown)
            self.dtc.Bind(wx.EVT_LEFT_UP, wxPanda.OnLeftUp)
            self.dtc.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
            self.dtc.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
            self.dtc.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
            self.dtc.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnTreeEndLabelEdit)
        else:

            # Build and display "project not set" warning
            tc = wx.StaticText(self, -1, 'Project directory not set', style=wx.ALIGN_CENTER)
            font = tc.GetFont()
            font.SetWeight(wx.FONTWEIGHT_BOLD)
            tc.SetFont(font)
            self.bs1.AddSpacer(10)
            self.bs1.Add(tc, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 2)

        self.bs1.Layout()

    def OnRightDown(self, evt):
        """
        This method does nothing. Oddly enough, *not* binding RightDown seems
        to affect RightUp's behaviour, and we only trap half the mouse up
        events.
        """
        pass

    def OnRightUp(self, evt):

        # Get the item under the mouse - bail if the item is not ok
        itemId = wxUtils.GetClickedItem(self.dtc, evt)
        if itemId is None or not itemId.IsOk():
            return

        menu = wx.Menu()
        mItem = wx.MenuItem(menu, wx.NewId(), 'Open in Explorer')
        menu.Append(mItem)
        wxUtils.IdBind(menu, wx.EVT_MENU, mItem.GetId(), self.OnOpenFile, itemId)
        self.PopupMenu(menu)
        menu.Destroy()

    def OnOpenFile(self, evt, itemId):
        systems = {
            'nt': os.startfile,
            'posix': lambda foldername: os.system('xdg-open "%s"' % foldername),
            'os2': lambda foldername: os.system('open "%s"' % foldername)
        }

        filePath = self.dtc.GetItemPath(itemId)
        dirPath = os.path.split(filePath)[0]
        systems.get(os.name, os.startfile)(dirPath)

    def OnMiddleDown(self, evt):

        # Get the item under the mouse - bail if the item is not ok.
        item_id = wxUtils.GetClickedItem(self.dtc, evt)
        if item_id is None or not item_id.IsOk():
            return

        # Select it and start drag and drop operations.
        self.dtc.SelectItem(item_id)
        get_base().drag_drop_manager.start(
            self,
            [self.dtc.GetItemPath(item_id)]
        )

    def OnLeftDClick(self, evt):

        # Load items
        itemId = wxUtils.GetClickedItem(self.dtc, evt)
        filePath = self.dtc.GetItemPath(itemId)
        ext = os.path.splitext(os.path.basename(self.dtc.GetItemText(itemId)))[1]
        if ext == '.xml':
            get_base().frame.OnFileOpen(None, filePath)
        elif ext == '.py':
            os.startfile(filePath)
            
    def OnTreeEndLabelEdit(self, evt):
        """Change the name of the asset in the system."""
        # Bail if no valid label is entered
        if not evt.GetLabel():
            evt.Veto()
            return
        
        # Construct new file path and rename
        oldPath = self.dtc.GetItemPath(evt.GetItem())
        head, tail = os.path.split(oldPath)
        newPath = os.path.join(head, evt.GetLabel())
        os.rename(oldPath, newPath)
        
    def OnUpdate(self, file_paths):
        """Rebuild the directory tree."""
        self.dtc.Freeze()
        
        def GetExpandedDict():
            
            # Return a dictionary mapping each node path to its tree item.
            expDict = {}
            for item in self.dtc.GetAllItems():
                dir = self.dtc.GetItemData(item)
                if dir is not None:
                    expDict[dir.directory] = (item, self.dtc.IsExpanded(item))
            return expDict
        
        # Get map of directory paths to items and expanded states before 
        # updating
        oldItems = GetExpandedDict()
        
        # Rebuild the tree control
        rootItem = self.dtc.GetRootItem()
        rootDirPath = self.dtc.GetItemData(rootItem).directory
        self.dtc._loadDir(rootItem, rootDirPath)
        
        # Get map of directory paths to items and expanded states after 
        # updating
        newItems = GetExpandedDict()
        
        # Set the expanded states back
        for dirPath, grp in oldItems.items():
            oldItem, oldExp = grp
            if dirPath in newItems and oldExp:
                newItem, newExp = newItems[dirPath]
                self.dtc.Expand(newItem)
        
        self.dtc.Thaw()
