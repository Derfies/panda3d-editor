import os

from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.attributes import TagAttribute
from game.nodes.constants import TAG_NODE_TYPE
from game.nodes.pandanode import PandaNode


class Prefab(PandaNode):

    fullpath = TagAttribute(
        required=True,
        read_only=True,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        full_path = kwargs.pop('fullpath', None)
        full_path = os.path.join(get_base().project.path, full_path)

        # This is a bit daft and proof I need to refactor the scene loader. Since
        # loading prefabs is essentially recursive scene loading, this is what we
        # have to do to get around the way scene loader manages its connections.
        old_nodes = get_base().scene_parser.nodes
        old_connections = get_base().scene_parser.connections
        prefab = get_base().scene_parser.load(full_path, None, load_connections=kwargs.pop('load_connections', False))
        get_base().scene_parser.nodes.update(old_nodes)
        get_base().scene_parser.connections.update(old_connections)

        # Bit crass. Need to rewrap the component returned by scene loader.
        comp = super().create(data=prefab.data)
        comp.fullpath = full_path
        comp.data.set_tag(TAG_NODE_TYPE, 'Prefab')
        return comp
