from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor.game.scene import Scene
from pandaEditor.game.nodes.constants import TAG_NODE_TYPE


class Scene(Scene):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.connections = {}
        
        # 'Create' the default NodePaths that come from showbase. Calling the
        # create method in this way doesn't generate any new NodePaths, it
        # will simply return those the default showbase creates when it starts
        # up. Tag them so their type is overriden and the component manager
        # wraps them appropriately.
        defaultCompTypes = [
            'Render',
            'BaseCamera',
            'BaseCam',
            'Render2d',
            'Aspect2d',
            'Pixel2d',
            'Camera2d',
            'Cam2d'
        ]
        for cType in defaultCompTypes:
            wrpr = get_base().node_manager.create(cType)
            wrpr.data.set_tag(TAG_NODE_TYPE, cType)
        
    def load(self, file_path):
        """Recreate a scene graph from file."""
        get_base().scene_parser.load(file_path)
    
    def save(self, file_path):
        """Save a scene graph to file."""
        get_base().scene_parser.save(self, file_path)
        
    def close(self):
        """Destroy the scene by removing all its components."""
        def destroy(comp):
            for child in comp.children:
                destroy(child)
            comp.destroy()
            
        destroy(get_base().node_manager.wrap(self))
        get_base().plugin_manager.on_scene_close()
        
        # Now remove the root node. If the root node was render, reset base
        # in order to remove and recreate the default node set.
        if self.rootNp is get_base().render:
            get_base().reset()

        self.rootNp.removeNode()
        
    def get_outgoing_connections(self, comp):
        """
        Return all outgoing connections for the indicated component.
        """
        return self.connections.get(comp.id, [])
    
    def get_incoming_connections(self, comp):
        """
        Return all incoming connections for the indicated component wrapper.
        """
        in_connections = []
        for comp_id, connections in self.connections.items():
            for connection in connections:
                if connection.srcComp == comp.data:
                    in_connections.append(connection)
        return in_connections
    
    def register_connection(self, source, target, name):
        """
        Register a connection to its target component. This allows us to find
        a connection and break it when a component is deleted.

        """
        print('register:', target.id, '->', source, name)
        self.connections.setdefault(target.id, set()).add((source, name))
    
    def deregister_connection(self, connection):
        comp = connection.parent
        comp_id = get_base().node_manager.wrap(comp).id
        if comp_id in self.connections:
            del self.connections[comp_id]
        
    # def clear_connections(self, comp):
    #     delIds = []
    #     for id, cnnctns in self.connections.items():
    #
    #         delCnnctns = []
    #         for cnnctn in cnnctns:
    #             if cnnctn.srcComp == comp:
    #                 delCnnctns.append(cnnctn)
    #
    #         for delCnnctn in delCnnctns:
    #             cnnctns.remove(delCnnctn)
    #
    #         if not cnnctns:
    #             delIds.append(id)
    #
    #     for delId in delIds:
    #         del self.connections[delId]