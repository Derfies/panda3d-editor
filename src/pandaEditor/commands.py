import uuid

import panda3d.core as pm
from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor.actions import (
    Add,
    Composite,
    Deselect,
    Parent,
    Remove,
    Select,
    SetAttribute,
    SetConnections,
)


def add(comps):
    """
    Create the add composite action, execute it and push it onto the undo 
    queue.

    """
    actions = []
    actions.append(Deselect(get_base().selection.comps))
    actions.extend([Add(comp) for comp in comps])
    actions.append(Select(comps))
    action = Composite(actions)
    get_base().action_manager.push(action)
    action()
    get_base().doc.on_modified(comps)
    

def remove(comps):
    """
    Create the remove composite action, execute it and push it onto the undo 
    queue.

    """
    actions = []
    actions.append(Deselect(comps))
    actions.extend([Remove(comp) for comp in comps])
    action = Composite(actions)
    get_base().action_manager.push(action)
    action()
    get_base().doc.on_modified(comps)
    

def duplicate(comps):
    """
    Create the duplicate composite action, execute it and push it onto the 
    undo queue.

    """
    sel_comps = get_base().selection.comps
    get_base().selection.clear()
    dupe_comps = [comp.duplicate() for comp in comps]
    actions = []
    actions.append(Deselect(sel_comps))
    actions.extend([Add(dupe_comp) for dupe_comp in dupe_comps])
    actions.append(Select(dupe_comps))
    action = Composite(actions)
    get_base().action_manager.push(action)
    action()
    get_base().doc.on_modified(dupe_comps)


def replace(fromComp, toComp):
    """
    
    """
    action = Composite([
        Deselect([fromComp]),
        Remove(fromComp),
        Add(toComp),
        Select([toComp])
    ])
    get_base().action_manager.push(action)
    action()
    get_base().doc.on_modified([fromComp, toComp])
    

def select(comps):
    """
    Create the select composite action, execute it and push it onto the
    undo queue.

    """
    action = Composite([
        Deselect(get_base().selection.comps),
        Select(comps)
    ])
    get_base().action_manager.push(action)
    action()
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


def parent(comps, pcomp):
    """
    Create the parent action, execute it and push it onto the undo queue.

    """
    action = Composite([Parent(comp, pcomp) for comp in comps])
    get_base().action_manager.push(action)
    action()
    get_base().doc.on_modified(comps)
    

def group(comps):
    """
    Create the group action, execute it and push it onto the undo queue.

    """
    from game.nodes.pandanode import PandaNode

    # Find the lowest common ancestor for all NodePaths - this will be the
    # parent for the group NodePath.
    common_np = comps[0].data.get_parent()
    nps = [comp.data for comp in comps]
    for np in nps:
        common_np = common_np.get_common_ancestor(np)
    common_comp = get_base().node_manager.wrap(common_np)

    group_comp = PandaNode.create(name='group')
    group_comp.id = str(uuid.uuid4())
    group_comp.parent = common_comp
    group_comp.set_default_values()
    
    actions = []
    actions.append(Add(group_comp))
    actions.extend([Parent(comp, group_comp) for comp in comps])
    actions.append(Deselect(comps))
    actions.append(Select([group_comp]))
    action = Composite(actions)
    get_base().action_manager.push(action)
    action()
    get_base().doc.on_modified(None)    # Complex scene change - full refresh required.
    

def ungroup(comps):
    """
    Create the ungroup action, execute it and push it onto the undo queue.

    """
    pcomps = []
    ccomp_sets = []
    for comp in comps:
        pcomps.append(comp.parent)
        ccomp_sets.append(comp.children)
        
    # Remove those nodes which were empty NodePaths.
    remove_comps = [
        comp
        for comp in comps
        if comp.data.node().isExactType(pm.PandaNode)
    ]
    
    actions = []
    actions.append(Deselect(comps))
    for i, ccomps in enumerate(ccomp_sets):
        actions.extend([Parent(ccomp, pcomps[i]) for ccomp in ccomps])
    actions.extend([Remove(comp) for comp in remove_comps])
    actions.append(Select([ccomp for ccomps in ccomp_sets for ccomp in ccomps]))
    
    action = Composite(actions)
    get_base().action_manager.push(action)
    action()
    get_base().doc.on_modified(None)    # Complex scene change - full refresh required.
