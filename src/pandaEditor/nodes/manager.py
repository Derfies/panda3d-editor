import logging

from game.nodes.attributes import Attribute
from game.nodes.manager import Manager as GameManager


logger = logging.getLogger(__name__)


class Manager(GameManager):

    def get_default_wrapper(self, comp):
        if hasattr(comp, 'getPythonTag'):
            return self.wrappers['NodePath']
        else:
            return self.wrappers['Base']
    '''
    def get_common_wrapper(self, comps):

        import inspect

        def isprop(v):
            return isinstance(v, Attribute)

        #propnames = [name for (name, value) in inspect.getmembers(comps[0], isprop)]
        # print('propnames:', propnames)
        #
        # print(comp_cls, comp_cls.mro(), comp_cls.__dict__)

        # Get method resolution orders for each wrapper for all the indicated
        # components.
        mros = []
        for comp in comps:
            comp_cls = self.GetWrapper(comp)
            if comp_cls is not None:
                mros.append(comp_cls.mro())
        if not mros:
            return self.get_default_wrapper(comps[0])

        # Intersect the mros to get the common classes.
        first_mro = mros[0]
        common_bases = sorted(
            set(first_mro).intersection(*mros),
            key=first_mro.index
        )

        # for cls in common_bases:
        #
        #     # print('->', inspect.getmembers(comp_cls, isprop))
        #     for name, prop in cls.__dict__.items():
        #         print(name, prop, type(prop))
        #     properties = {
        #         name: prop
        #         for name, prop in cls.__dict__.items()
        #         if isinstance(prop, Attribute)
        #     }
        #     print(properties)
        dicts = {}
        for base in reversed(common_bases):
            print(base, '->', base.__dict__)
            dicts.update(base.__dict__)
        dicts.update({'change_mro': False})

        try:
            common_wrapper = type(
                common_bases[0].__name__,
                tuple(common_bases),
                dicts#{'change_mro': False}
            )
        except TypeError as e:
            logger.error(f'Failed to create wrapper: {tuple(common_bases)}')
            raise
        common_base_names = [b.__name__ for b in common_bases]
        logger.info(f'Using bases for common wrapper: {common_base_names}')
        return common_wrapper
    '''

    def get_common_wrapper(self, comps):

        # Get method resolution orders for each wrapper for all the indicated
        # components.
        mros = []
        for comp in comps:
            wrprCls = self.GetWrapper(comp)
            if wrprCls is not None:
                mros.append(wrprCls.mro())

        if not mros:
            return self.get_default_wrapper(comps[0])

        # Intersect the mros to get the common classes.
        cmnClasses = set(mros[0]).intersection(*mros)

        # The result was unordered, so go find the first common class from
        # one of the mros.
        for cls in mros[0]:
            if cls in cmnClasses:
                return cls