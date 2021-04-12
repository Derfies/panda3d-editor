import logging
import inspect
from importlib import import_module

from panda3d.core import ConfigVariableBool


logger = logging.getLogger(__name__)


class WrapperMeta(type):

    def mro(cls):
        mro = super(WrapperMeta, cls).mro()
        editor_mode = ConfigVariableBool('editor_mode', False)
        if editor_mode:
            class_name = cls.__name__
            search_path = f'nodes.{class_name.lower()}'
            logger.info(f'Searching for: {search_path}')
            try:
                module = import_module(search_path)
            except ImportError as e:
                logger.error(f'Failed to find editor class: {search_path} {e}')
                return mro
            editor_cls = next(iter([
                value
                for name, value in inspect.getmembers(module, inspect.isclass)
                if name == class_name
            ]), None)
            if editor_cls is not None:
                mro = [editor_cls] + mro
                names = ', '.join([str(c) for c in mro])
                logger.info(f'Class: {cls.__name__} mro: {names}')

        return mro