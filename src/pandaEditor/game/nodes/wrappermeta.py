import logging
import inspect
from importlib import import_module

from panda3d.core import ConfigVariableBool


logger = logging.getLogger(__name__)


class WrapperMeta(type):

    def __new__(cls, cls_name, cls_bases, cls_dict):
        out_cls = super().__new__(cls, cls_name, cls_bases, cls_dict)
        if not hasattr(out_cls, 'change_mro'):
            out_cls.change_mro = True
        out_cls.__bases__ = out_cls.__bases__ + tuple()
        return out_cls

    def mro(cls):
        mro = super(WrapperMeta, cls).mro()
        change_mro = hasattr(cls, 'change_mro') and cls.change_mro
        if change_mro and ConfigVariableBool('editor_mode', False):

            class_name = cls.__name__
            path = cls.__module__.split('.')
            if path[0] != 'game':
                print('skip:', class_name)
                return mro
            path[0] = 'pandaEditor'
            search_path = '.'.join(path)
            #print(f'Searching for: {search_path}.{class_name}')

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
            if editor_cls is not None:
                #if cls.__name__ == 'Attribute':
                #    print(editor_cls.mro())
                #mro = [editor_cls] + mro
                print('EDITOR:', editor_cls.mro())
                print('GAME:', mro)
                mro = editor_cls.mro()[0:-1] + mro
                names = ', '.join([c.__name__ for c in mro])
                print(f'Component: {cls.__name__} mro: {names}')
        return mro