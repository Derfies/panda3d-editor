import logging

from game.nodes.manager import Manager as GameManager


logger = logging.getLogger(__name__)


class Manager(GameManager):

    def GetCommonWrapper(self, comps):
        # Get method resolution orders for each wrapper for all the indicated
        # components.
        mros = []
        for comp in comps:
            wrprCls = self.GetWrapper(comp)
            if wrprCls is not None:
                mros.append(wrprCls.mro())

        if not mros:
            # That's weird. Why pick the first one..?
            return self.GetDefaultWrapper(comps[0])

        # Intersect the mros to get the common classes.
        # for mro in mros:
        #     print('->', mro)
        # cmnClasses = set(mros[0]).intersection(*mros)
        # print('cmnClasses:', cmnClasses)
        #
        # print('USING:', mros[0])

        first_mro = mros[0]
        foo = sorted(set(first_mro).intersection(*mros), key=first_mro.index)
        print('foo:', foo)
        return type(foo[0].__name__, tuple(foo), {})
        return foo[0]

        # The result was unordered, so go find the first common class from
        # one of the mros.
        # for cls in mros[0]:
        #     if cls in cmnClasses:
        #         # BUG - Assumes proper hierarchy made from editor class imports.
        #         print('RETURNING:', cls, '->', cls.mro())
        #         return cls