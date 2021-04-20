import inspect
import logging
from importlib import import_module

from panda3d.core import ConfigVariableBool


logger = logging.getLogger(__name__)


class BaseMetaClass(type):

    def __new__(metacls, name, bases, attrs):
        cls = super().__new__(metacls, name, bases, attrs)
        if not hasattr(cls, 'change_mro'):
            cls.change_mro = True
        cls.__bases__ = cls.__bases__ + tuple()
        return cls

    def mro(cls):
        change_mro = (
            getattr(cls, 'change_mro', False) and
            ConfigVariableBool('editor_mode', False)
        )
        mro = super().mro()
        return cls.get_mro(cls, mro) if change_mro else mro

    @classmethod
    def get_mro(metacls, cls, mro):
        class_name = cls.__name__
        path = cls.__module__.split('.')
        if path[0] != 'game':

            # STILL ATTEMPTING TO WRAP HERE AFTER THE FACT
            print('skip:', class_name, '->', path, getattr(cls, 'change_mro', False))
            return mro
        path[0] = 'pandaEditor'
        search_path = '.'.join(path)

        try:
            module = import_module(search_path)
        except ModuleNotFoundError as e:

            # TODO: Set a flag here so we're not continually trying to
            # load a module that's not there.
            print(e)
            return mro
        editor_cls = next(iter([
            value
            for name, value in inspect.getmembers(module, inspect.isclass)
            if name == class_name
        ]), None)
        if editor_cls is None:
            return mro

        # Ignore the last mro "object" as it's common to both.
        mro = editor_cls.mro()[0:-1] + mro
        names = ', '.join([c.__name__ for c in mro])
        logger.info(f'Component: {cls.__name__} mro: {names}')

        return mro

