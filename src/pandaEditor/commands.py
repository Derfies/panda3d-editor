import wx

import actions


def Add( nps ):
    """
    Create the add composite action, execute it and push it onto the
    undo queue.
    """
    actns = [
        actions.Deselect( wx.GetApp(), wx.GetApp().selection.nps ),
        actions.Add( wx.GetApp(), nps ), 
        actions.Select( wx.GetApp(), nps )
    ]
    comp = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( comp )
    comp()
    

def Duplicate( nps ):
    """
    Duplicate the indicated node paths once they've been deselected, then
    create an add action and push it onto the undo queue.
    """
    # Record the current selection then clear it
    selNps = wx.GetApp().selection.nps
    wx.GetApp().selection.Clear()
    
    # Duplicate the indicated node paths
    dupeNps = wx.GetApp().scene.DuplicateNodePaths( selNps )
    
    # Reset the selection and run add
    wx.GetApp().selection.Add( selNps )
    Add( dupeNps )
    

def Remove( nps ):
    """
    Create the remove composite action, execute it and push it onto the
    undo queue.
    """
    actns = [
        actions.Deselect( wx.GetApp(), nps ), 
        actions.Remove( wx.GetApp(), nps )
    ]
    comp = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( comp )
    comp()
    

def Select( nps ):
    """
    Create the select composite action, execute it and push it onto the
    undo queue.
    """
    actns = [
        actions.Deselect( wx.GetApp(), wx.GetApp().selection.nps ), 
        actions.Select( wx.GetApp(), nps )
    ]
    comp = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( comp )
    comp()
    

def SetAttribute( nps, attr, val ):
    """
    Create the set attribute action, execute it and push it onto the undo
    queue.
    """
    actn = actions.SetAttribute( wx.GetApp(), nps, attr, val )
    wx.GetApp().actnMgr.Push( actn )
    actn()
    

def Parent( nps, parent ):
    """
    Create the parent action, execute it and push it onto the undo queue.
    """
    actn = actions.Parent( wx.GetApp(), nps, parent )
    wx.GetApp().actnMgr.Push( actn )
    actn()