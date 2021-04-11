import wx
import panda3d.core as pm

from pandaEditor import actions


def Add(comps):
    """
    Create the add composite action, execute it and push it onto the undo 
    queue.
    """
    actns = []
    actns.append(actions.Deselect(base.selection.comps))
    actns.extend([actions.Add(comp) for comp in comps])
    actns.append(actions.Select(comps))
    
    actn = actions.Composite(actns)
    base.frame.app.actnMgr.Push(actn)
    actn()
    base.frame.app.doc.OnModified(comps)
    

def Remove(comps):
    """
    Create the remove composite action, execute it and push it onto the undo 
    queue.
    """
    actns = []
    actns.append(actions.Deselect(comps))
    actns.extend([actions.Remove(comp) for comp in comps])
    actn = actions.Composite(actns)
    base.frame.app.actnMgr.Push(actn)
    actn()
    base.frame.app.doc.OnModified(comps)
    

def Duplicate(comps):
    """
    Create the duplicate composite action, execute it and push it onto the 
    undo queue.
    """
    selComps = base.selection.comps
    base.selection.Clear()
    
    dupeComps = []
    for comp in comps:
        wrpr = base.game.nodeMgr.Wrap(comp)
        dupeComps.append(wrpr.Duplicate())
        
    actns = []
    actns.append(actions.Deselect(selComps))
    actns.extend([actions.Add(dupeComp) for dupeComp in dupeComps])
    actns.append(actions.Select(dupeComps))
    
    actn = actions.Composite(actns)
    base.frame.app.actnMgr.Push(actn)
    actn()
    base.frame.app.doc.OnModified(dupeComps)
    

def Replace(fromComp, toComp):
    """
    
    """
    actns = [
        actions.Deselect([fromComp]),
        actions.Remove(fromComp),
        actions.Add(toComp),
        actions.Select([toComp])
    ]
    
    actn = actions.Composite(actns)
    base.frame.app.actnMgr.Push(actn)
    actn()
    base.frame.app.doc.OnModified([fromComp, toComp])
    

def Select(comps):
    """
    Create the select composite action, execute it and push it onto the
    undo queue.
    """
    actns = [
        actions.Deselect(base.selection.comps), 
        actions.Select(comps)
    ]
    
    actn = actions.Composite(actns)
    base.frame.app.actnMgr.Push(actn)
    actn()
    base.frame.app.doc.OnRefresh(comps)
    

def SetAttribute(comps, attrs, val):
    """
    Create the set attribute action, execute it and push it onto the undo
    queue.
    """
    actns = [actions.SetAttribute(comps[i], attrs[i], val) for i in range(len(comps))]
    
    actn = actions.Composite(actns)
    base.frame.app.actnMgr.Push(actn)
    actn()
    base.frame.app.doc.OnModified(comps)
    

def Parent(comps, pComp):
    """
    Create the parent action, execute it and push it onto the undo queue.
    """
    actns = [actions.Parent(comp, pComp) for comp in comps]
    
    actn = actions.Composite(actns)
    base.frame.app.actnMgr.Push(actn)
    actn()
    base.frame.app.doc.OnModified(comps)
    

def Unparent():
    pass
    

def Group(nps):
    """
    Create the group action, execute it and push it onto the undo queue.
    """
    # Find the lowest common ancestor for all NodePaths - this will be the
    # parent for the group NodePath.
    cmmnNp = nps[0].getParent()
    for np in nps:
        cmmnNp = cmmnNp.getCommonAncestor(np)
    
    grpNp = pm.NodePath('group')
    grpNp.reparentTo(cmmnNp)
    
    actns = []
    actns.append(actions.Add(grpNp))
    actns.extend([actions.Parent(np, grpNp) for np in nps])
    actns.append(actions.Deselect(nps))
    actns.append(actions.Select([grpNp]))
    
    actn = actions.Composite(actns)
    base.frame.app.actnMgr.Push(actn)
    actn()
    base.frame.app.doc.OnModified(nps.append(grpNp))
    

def Ungroup(nps):
    """
    Create the ungroup action, execute it and push it onto the undo queue.
    """
    pNps = []
    cNpSets = []
    for np in nps:
        wrpr = base.game.nodeMgr.Wrap(np)
        pNps.append(wrpr.GetParent().data)
        cNpSets.append([cWrpr.data for cWrpr in wrpr.GetChildren()])
        
    # Remove those nodes which were empty NodePaths.
    rmvNps = [np for np in nps if np.node().isExactType(pm.PandaNode)]
    
    actns = []
    actns.append(actions.Deselect(nps))
    for i, cNps in enumerate(cNpSets):
        actns.extend([actions.Parent(cNp, pNps[i]) for cNp in cNps])
    actns.extend([actions.Remove(np) for np in rmvNps])
    actns.append(actions.Select([cNp for cNps in cNpSets for cNp in cNps]))
    
    actn = actions.Composite(actns)
    base.frame.app.actnMgr.Push(actn)
    actn()
    base.frame.app.doc.OnModified(nps.append(rmvNps))
    

def Connect(tgtComps, cnnctn, fn):
    """
    Create the connect action, execute it and push it onto the undo queue.
    """
    actn = actions.Connect(tgtComps, cnnctn, fn)
    base.frame.app.actnMgr.Push(actn)
    actn()
    base.frame.app.doc.OnModified()
    

def SetConnections(tgtComps, cnnctns):
    """
    Create the connect action, execute it and push it onto the undo queue.
    """
    actns = [actions.SetConnections(tgtComps, cnnctn) for cnnctn in cnnctns]
    
    actn = actions.Composite(actns)
    base.frame.app.actnMgr.Push(actn)
    actn()
    base.frame.app.doc.OnModified()