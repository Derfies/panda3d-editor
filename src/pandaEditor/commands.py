import panda3d.core as pm
from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor import actions
from pandaEditor.actions import (
    Composite,
    #Connect,
    SetAttribute,
    SetConnections,
)


def Add(comps):
    """
    Create the add composite action, execute it and push it onto the undo 
    queue.

    """
    actns = []
    actns.append(actions.Deselect(get_base().selection.comps))
    actns.extend([actions.Add(comp) for comp in comps])
    actns.append(actions.Select(comps))
    actn = actions.Composite(actns)
    get_base().action_manager.push(actn)
    actn()
    get_base().doc.on_modified(comps)
    

def Remove(comps):
    """
    Create the remove composite action, execute it and push it onto the undo 
    queue.

    """
    actns = []
    actns.append(actions.Deselect(comps))
    actns.extend([actions.Remove(comp) for comp in comps])
    actn = actions.Composite(actns)
    get_base().action_manager.push(actn)
    actn()
    get_base().doc.on_modified(comps)
    

def Duplicate(comps):
    """
    Create the duplicate composite action, execute it and push it onto the 
    undo queue.

    """
    sel_comps = get_base().selection.comps
    get_base().selection.clear()
    dupe_comps = [
        comp.duplicate()
        for comp in comps
    ]
    actns = []
    actns.append(actions.Deselect(sel_comps))
    actns.extend([actions.Add(dupeComp) for dupeComp in dupe_comps])
    actns.append(actions.Select(dupe_comps))
    actn = actions.Composite(actns)
    get_base().action_manager.push(actn)
    actn()
    get_base().doc.on_modified(dupe_comps)
    

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
    get_base().action_manager.push(actn)
    actn()
    get_base().doc.on_modified([fromComp, toComp])
    

def Select(comps):
    """
    Create the select composite action, execute it and push it onto the
    undo queue.

    """
    actns = [
        actions.Deselect(get_base().selection.comps), 
        actions.Select(comps)
    ]
    actn = actions.Composite(actns)
    get_base().action_manager.push(actn)
    actn()
    get_base().doc.on_refresh(comps)
    

def set_attribute(comps, name, value):
    """
    Create the set attribute action, execute it and push it onto the undo
    queue.

    """
    action = Composite([
        SetAttribute(comp, name, value)
        for comp in comps
    ])
    get_base().action_manager.push(action)
    action()
    get_base().doc.on_modified(comps)


# def connect(comps, name, value):
#     """
#     Create the connect action, execute it and push it onto the undo queue.
#
#     """
#     action = Composite([
#         Connect(comp, name, value)
#         for comp in comps
#     ])
#     get_base().action_manager.push(action)
#     action()
#     get_base().doc.on_modified()


def set_connections(comps, name, value):
    """
    Create the connect action, execute it and push it onto the undo queue.

    """
    action = Composite([
        SetConnections(comp, name, value)
        for comp in comps
    ])
    get_base().action_manager.push(action)
    action()
    get_base().doc.on_modified()


def Parent(comps, pComp):
    """
    Create the parent action, execute it and push it onto the undo queue.

    """
    actns = [actions.Parent(comp, pComp) for comp in comps]
    actn = actions.Composite(actns)
    get_base().action_manager.push(actn)
    actn()
    get_base().doc.on_modified(comps)
    

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
    get_base().action_manager.push(actn)
    actn()
    get_base().doc.on_modified(nps.append(grpNp))
    

def Ungroup(nps):
    """
    Create the ungroup action, execute it and push it onto the undo queue.

    """
    pNps = []
    cNpSets = []
    for np in nps:
        wrpr = get_base().node_manager.wrap(np)
        pNps.append(wrpr.parent.data)
        cNpSets.append([cWrpr.data for cWrpr in wrpr.children])
        
    # Remove those nodes which were empty NodePaths.
    rmvNps = [np for np in nps if np.node().isExactType(pm.PandaNode)]
    
    actns = []
    actns.append(actions.Deselect(nps))
    for i, cNps in enumerate(cNpSets):
        actns.extend([actions.Parent(cNp, pNps[i]) for cNp in cNps])
    actns.extend([actions.Remove(np) for np in rmvNps])
    actns.append(actions.Select([cNp for cNps in cNpSets for cNp in cNps]))
    
    actn = actions.Composite(actns)
    get_base().action_manager.push(actn)
    actn()
    get_base().doc.on_modified(nps.append(rmvNps))
