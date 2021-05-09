import logging

import panda3d.core as pc

from game.nodes.manager import Manager as GameManager


logger = logging.getLogger(__name__)


class Manager(GameManager):

    def get_default_wrapper(self, obj):
        if isinstance(obj, pc.NodePath):
            return self.wrappers['NodePath']
        else:
            return self.wrappers['NonGraphObject']

    def get_common_wrapper(self, comps):

        # Get method resolution orders for each wrapper for all the indicated
        # components.
        mros = []
        for comp in comps:
            comp_cls = self.get_wrapper(comp.data)
            if comp_cls is not None:
                mros.append(comp_cls.__mro__)
        if not mros:
            return self.get_default_wrapper(comps[0].data)

        # Intersect the mros to get the common classes.
        first_mro = mros[0]
        common_bases = sorted(
            set(first_mro).intersection(*mros),
            key=first_mro.index
        )

        dicts = {}
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
