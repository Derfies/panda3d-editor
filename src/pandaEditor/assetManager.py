import copy
import logging
import os

import panda3d.core as pm
from direct.showbase.PythonUtil import getBase as get_base


logger = logging.getLogger(__name__)


class AssetManager:
        
    def on_asset_modified(self, file_paths):
        """
        Reload the indicated file paths as they have been marked as dirty in
        the project directory.

        """
        for file_path in file_paths:
            
            # Bail if the path is a directory.
            if os.path.isdir(file_path):
                continue
            panda_path = pm.Filename.from_os_specific(file_path)
            
            # Test if the file path represents an asset in one of Panda's
            # asset pools.
            if pm.TexturePool.hasTexture(panda_path):
                logger.info(f'Reloading texture: {panda_path}')
                self.reload_texture(panda_path)
            elif pm.ModelPool.hasModel(panda_path):
                logger.info(f'Reloading model: {panda_path}')
                self.reload_model(panda_path)
        
    def reload_texture(self, full_path):
        for tex in pm.TexturePool.find_all_textures():
            if tex.get_fullpath() == full_path:
                tex.reload()
                
    def reload_model(self, panda_path):

        # Load the new model.
        comp_cls = get_base().node_manager.get_component_by_name('ModelRoot')
        new_np = get_base().loader.load_model(panda_path, noCache=True)
        new_comp = comp_cls.create(data=new_np)

        # Find all instances of this model in the scene graph.
        comps = [
            get_base().node_manager.wrap(np)
            for np in get_base().scene.rootNp.find_all_matches('**/+ModelRoot')
            if np.node().get_fullpath() == panda_path
        ]

        for comp in comps:

            # Replace the node in the hierarchy.
            # TODO: Could move this to editor method insert_child.
            index = comp.sibling_index
            parent_np = comp.parent.data
            children = list(parent_np.get_children())
            for child in children:
                child.detach_node()
            children.pop(index)
            copy_np = copy.deepcopy(new_np)
            children.insert(index, copy_np)
            for child in children:
                child.reparent_to(parent_np)

            copy_comp = get_base().node_manager.wrap(copy_np)

            # Set properties on the new node to match the one it's replacing.
            for name, value in comp.attributes.items():
                try:
                    setattr(copy_comp, name, value)
                except Exception as e:
                    logger.error(
                        f'Failed to set attribute on replaced component: '
                        f'{copy_np}.{name}',
                        exc_info=True,
                    )

            # Set connections on the new node to match the one it's replacing.
            for name, value in comp.connections.items():
                try:
                    if comp.__class__.connections[name].many:
                        getattr(copy_comp, name)[:] = value
                    else:
                        setattr(copy_comp, name, value)
                except Exception as e:
                    logger.error(
                        f'Failed to set connection on replaced component: '
                        f'{copy_np}.{name}',
                        exc_info=True,
                    )

            # Required since we loaded the model with no cache.
            copy_np.node().fullpath = panda_path

        get_base().doc.on_modified()
