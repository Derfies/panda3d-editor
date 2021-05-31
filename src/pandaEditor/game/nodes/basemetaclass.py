import inspect
import logging
from importlib import import_module

from panda3d.core import ConfigVariableBool


logger = logging.getLogger(__name__)


class BaseMetaClass(type):

    def __new__(metacls, name, bases, attrs):

        # Run once per class only. Will run for every new component selection
        # because the scene graph is dynamically creating types.
        cls = super().__new__(metacls, name, bases, attrs)
        if not hasattr(cls, 'change_mro'):
            cls.change_mro = True
        cls.__bases__ = cls.__bases__ + tuple()
        return cls

    def mro(cls):
        """
        Called every time class.mro() is called - NOT once during class
        creation. Don't call mro() in your own code, use __mro__ instead.

        """
        change_mro = bool(
            getattr(cls, 'change_mro', False) and
            ConfigVariableBool('editor_mode', False)
        )
        mro = super().mro()

        # TODO: Might want to try and cache the results here so we don't have
        # to run this method every time mro() is called.
        if change_mro:
            return cls.get_mro(cls, mro)
        return mro

    @classmethod
    def get_mro(metacls, cls, mro):
        class_name = cls.__name__
        path = cls.__module__.split('.')

        # Don't attempt to mix in anything but game classes.
        if path[0] != 'game':
            logger.info(f'Ignoring mixin for class: {".".join(path)}.{class_name}')
            return mro
        path[0] = 'pandaEditor'
        search_path = '.'.join(path)

        try:
            module = import_module(search_path)
        except ModuleNotFoundError as e:

            # TODO: Set a flag here so we're not continually trying to
            # load a module that's not there.
            logger.warning(f'Editor module not found: {search_path}')
            return mro

        editor_cls = next(iter([
            value
            for name, value in inspect.getmembers(module, inspect.isclass)
            if name == class_name
        ]), None)
        if editor_cls is None:
            logger.info(f'Could not find editor class: {class_name}')
            return mro

        # Ignore the last mro "object" as it's common to both.
        mro = list(editor_cls.__mro__[0:-1]) + mro
        names = ', '.join([c.__name__ for c in mro])
        logger.info(f'Component: {cls.__name__} mro: {names}')
        return mro
