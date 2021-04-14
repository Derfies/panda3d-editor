import logging

from game.nodes.manager import Manager as GameManager


logger = logging.getLogger(__name__)


class Manager(GameManager):

    def get_common_wrapper(self, comps):

        # Get method resolution orders for each wrapper for all the indicated
        # components.
        mros = []
        for comp in comps:
            wrpr_cls = self.GetWrapper(comp)
            if wrpr_cls is not None:
                mros.append(wrpr_cls.mro())
        if not mros:
            return self.GetDefaultWrapper(comps[0])

        # Intersect the mros to get the common classes.
        first_mro = mros[0]
        common_bases = sorted(
            set(first_mro).intersection(*mros),
            key=first_mro.index
        )
        try:
            common_wrapper = type(
                common_bases[0].__name__,
                tuple(common_bases),
                {'change_mro': False}
            )
        except TypeError as e:
            logger.error(f'Failed to create wrapper: {tuple(common_bases)}')
            raise
        common_base_names = [b.__name__ for b in common_bases]
        logger.info(f'Using bases for common wrapper: {common_base_names}')
        return common_wrapper
