import wx
import pandac.PandaModules as pm

import actions


def Add( comps ):
    """
    Create the add composite action, execute it and push it onto the undo 
    queue.
    """
    actns = []
    actns.append( actions.Deselect( base.selection.nps ) )
    actns.extend( [actions.Add( comp ) for comp in comps] )
    actns.append( actions.Select( comps ) )
    
    actn = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( actn )
    actn()
    wx.GetApp().doc.OnModified()
    

def Remove( comps ):
    """
    Create the remove composite action, execute it and push it onto the undo 
    queue.
    """
    actns = []
    actns.append( actions.Deselect( comps ) )
    actns.extend( [actions.Remove( comp ) for comp in comps] )
    
    actn = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( actn )
    actn()
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
    

def Replace( fromComp, toComp ):
    """
    
    """
    actns = [
        actions.Deselect( [fromComp] ),
        actions.Remove( fromComp ),
        actions.Add( toComp ),
        actions.Select( [toComp] )
    ]
    
    actn = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( actn )
    actn()
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
    
    actn = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( actn )
    actn()
    wx.GetApp().doc.OnRefresh()
    

def SetAttribute( comps, attrs, val ):
    """
    Create the set attribute action, execute it and push it onto the undo
    queue.
    """
    actns = [actions.SetAttribute( comps[i], attrs[i], val ) for i in range( len( comps ) )]
    
    actn = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( actn )
    actn()
    wx.GetApp().doc.OnModified()
    

def Parent( nps, parent ):
    """
    Create the parent action, execute it and push it onto the undo queue.
    """
    actns = [actions.Parent( np, parent ) for np in nps]
    
    actn = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( actn )
    actn()
    wx.GetApp().doc.OnModified()
    

def Group( nps ):
    """
    Create the group action, execute it and push it onto the undo queue.
    """
    grpNp = pm.NodePath( 'group' )
    grpNp.reparentTo( base.scene.rootNp )
    
    actns = []
    actns.append( actions.Add( grpNp ) )
    actns.extend( [actions.Parent( np, grpNp ) for np in nps] )
    actns.append( actions.Deselect( nps ) )
    actns.append( actions.Select( [grpNp] ) )
    
    actn = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( actn )
    actn()
    wx.GetApp().doc.OnModified()
    

def Ungroup( nps ):
    """
    Create the ungroup action, execute it and push it onto the undo queue.
    """
    childNps = []
    for np in nps:
        wrpr = base.game.nodeMgr.Wrap( np )
        childNps.extend( [cWrpr.data for cWrpr in wrpr.GetChildren()] )
    removeNps = [np for np in nps if np.node().isOfType( pm.PandaNode )]
    
    actns = []
    actns.append( actions.Deselect( nps ) )
    actns.extend( [actions.Parent( childNp, base.scene.rootNp ) for childNp in childNps] )
    actns.extend( [actions.Remove( np ) for np in removeNps] )
    actns.append( actions.Select( childNps ) )
    
    actn = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( actn )
    actn()
    wx.GetApp().doc.OnModified()
    
    
def Parent():pass


def Unparent(): pass
    

def Connect( tgtComps, cnnctn, fn ):
    """
    Create the connect action, execute it and push it onto the undo queue.
    """
    actn = actions.Connect( tgtComps, cnnctn, fn )
    wx.GetApp().actnMgr.Push( actn )
    actn()
    wx.GetApp().doc.OnModified()
    

def SetConnections( tgtComps, cnnctns ):
    """
    Create the connect action, execute it and push it onto the undo queue.
    """
    actns = [actions.SetConnections( tgtComps, cnnctn ) for cnnctn in cnnctns]
    
    actn = actions.Composite( actns )
    wx.GetApp().actnMgr.Push( actn )
    actn()
    wx.GetApp().doc.OnModified()