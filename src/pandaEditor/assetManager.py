import abc
import copy
import logging

import panda3d.core as pm
from direct.showbase.PythonUtil import getBase as get_base


logger = logging.getLogger(__name__)


class ReloaderBase(metaclass=abc.ABCMeta):

    def __init__(self, file_path):
        self.file_path = file_path
        self.panda_path = pm.Filename.from_os_specific(file_path)

    @staticmethod
    @abc.abstractmethod
    def is_asset_used(panda_path):
        """"""

    @abc.abstractmethod
    def get_instances(self):
        """"""

    @abc.abstractmethod
    def reload_instance(self, instance):
        """"""

    def run(self):
        cls_name = self.__class__.__name__
        logger.info(f'{cls_name} reloading asset: {self.panda_path}')
        for instance in self.get_instances():
            logger.info(f'{cls_name} reloading instance: {self.panda_path}')
            self.reload_instance(instance)


class TextureReloader(ReloaderBase):

    @staticmethod
    def is_asset_used(file_path):
        panda_path = pm.Filename.from_os_specific(file_path)
        return pm.TexturePool.has_texture(panda_path)

    def get_instances(self):
        return [
            tex
            for tex in pm.TexturePool.find_all_textures()
            if tex.get_fullpath() == self.panda_path
        ]

    def reload_instance(self, instance):
        instance.reload()


class ModelReloader(ReloaderBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the new model.
        comp_cls = get_base().node_manager.get_component_by_name('ModelRoot')
        self.new_np = get_base().loader.load_model(self.panda_path, noCache=True)
        self.new_comp = comp_cls.create(data=self.new_np)

    @staticmethod
    def is_asset_used(file_path):
        panda_path = pm.Filename.from_os_specific(file_path)
        return pm.ModelPool.has_model(panda_path)

    def get_instances(self):
        return [
            get_base().node_manager.wrap(np)
            for np in get_base().scene.rootNp.find_all_matches('**/+ModelRoot')
            if np.node().get_fullpath() == self.panda_path
        ]

    def reload_instance(self, comp):

        # Replace the node in the hierarchy.
        # TODO: Could move this to editor method insert_child.
        index = comp.sibling_index
        parent_np = comp.parent.data
        children = list(parent_np.get_children())
        for child in children:
            child.detach_node()
        children.pop(index)
        copy_np = copy.deepcopy(self.new_np)
        children.insert(index, copy_np)
        for child in children:
            child.reparent_to(parent_np)

        copy_comp = get_base().node_manager.wrap(copy_np)

        # Set properties on the new node to match the one it's replacing.
        for name, value in comp.attributes.items():
            try:
                setattr(copy_comp, name, value)
                logging.info(f'Set attribute: {copy_comp.data}.{name} -> {value}')
            except Exception as e:
                logger.error(
                    f'Failed to set attribute on replaced component: '
                    f'{copy_np}.{name}',
                    exc_info=True,
                )

        # Set connections on the new node to match the one it's replacing.
        # TODO: Connections going the other way still broken.
        for name, value in comp.connections.items():
            try:
                if comp.__class__.connections[name].many:
                    getattr(copy_comp, name)[:] = value
                else:
                    setattr(copy_comp, name, value)
                logging.info(f'Set attribute: {copy_comp.data}.{name} -> {value}')
            except Exception as e:
                logger.error(
                    f'Failed to set connection on replaced component: '
                    f'{copy_np}.{name}',
                    exc_info=True,
                )

        # Required since we loaded the model with no cache.
        copy_np.node().fullpath = self.panda_path


        # HAXXOR - do this after
        get_base().doc.on_modified()


class AssetManager:

    def __init__(self):
        self.reloaders = [
            TextureReloader,
            ModelReloader,
        ]
        
    def on_asset_modified(self, file_paths):
        """
        Reload the indicated file paths as they have been marked as dirty in
        the project directory.

        """
        for reloader_cls in self.reloaders:
            for file_path in file_paths:
                if not reloader_cls.is_asset_used(file_path):
                    continue
                reloader = reloader_cls(file_path)
                reloader.run()
