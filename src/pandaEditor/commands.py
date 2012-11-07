import wx

import actions


def Add( nps ):
    """
    Create the add composite action, execute it and push it onto the
    undo queue.
    """
    actns = [
        actions.Deselect( base.selection.nps ),
        actions.Add( nps ), 
        actions.Select( nps )
    ]
    comp = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( comp )
    comp()
    wx.GetApp().doc.OnModified()
    

def Duplicate( nps ):
    """
    Duplicate the indicated node paths once they've been deselected, then
    create an add action and push it onto the undo queue.
    """
    # Record the current selection then clear it
    selNps = base.selection.nps
    base.selection.Clear()
    
    # Duplicate the indicated node paths
    dupeNps = base.scene.DuplicateNodePaths( selNps )
    
    # Reset the selection and run add
    base.selection.Add( selNps )
    Add( dupeNps )
    wx.GetApp().doc.OnModified()
    

def Remove( nps ):
    """
    Create the remove composite action, execute it and push it onto the
    undo queue.
    """
    actns = [
        actions.Deselect( nps ), 
        actions.Remove( nps )
    ]
    comp = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( comp )
    comp()
    wx.GetApp().doc.OnModified()
    

def Select( nps ):
    """
    Create the select composite action, execute it and push it onto the
    undo queue.
    """
    actns = [
        actions.Deselect( base.selection.nps ), 
        actions.Select( nps )
    ]
    comp = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( comp )
    comp()
    wx.GetApp().doc.OnRefresh()
    

def SetAttribute( nps, attr, val ):
    """
    Create the set attribute action, execute it and push it onto the undo
    queue.
    """
    actn = actions.SetAttribute( nps, attr, val )
    wx.GetApp().actnMgr.Push( actn )
    actn()
    wx.GetApp().doc.OnModified()
    

def Parent( nps, parent ):
    """
    Create the parent action, execute it and push it onto the undo queue.
    """
    actn = actions.Parent( nps, parent )
    wx.GetApp().actnMgr.Push( actn )
    actn()
    wx.GetApp().doc.OnModified()