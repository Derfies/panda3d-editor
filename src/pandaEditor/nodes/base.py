from direct.showbase.PythonUtil import getBase as get_base

from game.utils import get_lower_camel_case


class Base:

    @property
    def name_(self):

        # TODO: Rename to "display_name" or similar.
        try:
            return getattr(self, 'name')
        except Exception as e:
            return get_lower_camel_case(self.data.__class__.__name__)

    def validate_drag_drop(self, dragComp, dropComp):
        return False
    
    def get_attrib(self):
        """
        Return a dictionary with bare minimum data for a component - its type
        and id.
        """
        attrib = {
            'id': self.id,
            'type': self.type,
        }
        if attrib['id'] is None:
            del attrib['id']
        return attrib
        
    # def get_property_data(self):
    #     """
    #     Return a dictionary of all properties as key / value pairs. Make sure
    #     that values have been serialised to string.
    #     """
    #     propDict = {}
    #     for attr in self.attributes.values():
    #         if attr.serialise and not isinstance(attr, Connection):
    #             propDict[attr.name] = cUtils.serialise(attr.get())
    #     return propDict
    
    # def get_connection_data(self):
    #     cnnctnDict = {}
    #
    #     # Put this component's connections into key / value pairs.
    #     for cnnctn in self.connections:
    #         comps = cnnctn.get()
    #         if comps is None:
    #             continue
    #
    #         ids = []
    #         try:
    #             for comp in comps:
    #                 wrpr = get_base().node_manager.wrap(comp)
    #                 ids.append(wrpr.id)
    #         except TypeError as e:
    #             wrpr = get_base().node_manager.wrap(comps)
    #             ids.append(wrpr.id)
    #         cnnctnDict[cnnctn.name] = ids
    #
    #     return cnnctnDict

    @property
    def modified(self):
        return False

    @modified.setter
    def modified(self, value):
        pass

    @property
    def savable(self):
        return True
    
    def on_select(self):
        pass
    
    def on_deselect(self):
        pass
    
    def on_drag_drop(self, dragComp, dropComp):
        pass
    
    # def connect(self, comps, mode):
    #     if mode in cnnctnMap:
    #         cnnctn = cnnctnMap[mode](self.data, comps)
    #         cnnctn.connect()
    
    def is_of_type(self, type_):
        return type_ in self.data.__class__.mro()
    
    def get_possible_connections(self, comps):
        """
        Return a list of connections that can be made with the given 
        components.
        """
        connections = []
        
        for comp in comps:
            wrpr = get_base().node_manager.wrap(comp)
            #posCnnctns = [attr for attr in self.get_attributes() if hasattr(attr, 'cnnctn')]
            #posCnnctns.extend(self.connections)
            for connection in self.connections:
                if (
                    wrpr.is_of_type(connection.type) and
                    connection not in connections
                ):
                    connections.append(connection)
        
        return connections
    
    def set_default_values(self):
        pass

    @property
    def default_parent(self):
        return get_base().node_manager.wrap(get_base().scene)
    
    # @classmethod
    # def get_default_property_data(cls):
    #     try:
    #         defPropDict = cls.create().get_property_data()
    #     except:
    #         defPropDict = {}
    #     return defPropDict
    
    def get_sibling_index(self):
        """
        Return the position of of this wrapper's component amongst its sibling
        components.
        """
        parent = self.parent
        if parent is None:
            return None
        #objs = [child.data for child in parent.children]
        # try:
        print('parent:', parent)
        print('children:', parent.children)
        return parent.children.index(self)
        # except ValueError:
        #     print('objs:', objs, 'find:', self.data, [type(o) for o in objs])
        #     raise
