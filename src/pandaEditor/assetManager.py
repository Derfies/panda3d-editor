import logging
import collections
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
        
    def reload_texture(self, panda_path):
        for tex in pm.TexturePool.find_all_textures():
            if tex.get_filename() == panda_path:
                tex.reload()
                
    def reload_model(self, panda_path):

        # Reload the model in the model pool.
        # pm.ModelPool.release_model(panda_path)
        # pm.ModelPool.load_model(panda_path)

        comp_cls = get_base().node_manager.get_component_by_name('ModelRoot')
        # file_path = pm.Filename.to_os_specific(panda_path)
        # comp = comp_cls.create(model_path=file_path)
        new_np = get_base().loader.load_model(panda_path, noCache=True)
        new_comp = comp_cls.create(data=new_np)

        # Find all instances of this model in the scene graph.
        comps = [
            get_base().node_manager.wrap(np)
            for np in get_base().scene.rootNp.find_all_matches('**/+ModelRoot')
            if np.node().get_fullpath() == panda_path
        ]
        
        # Now unhook all the NodePaths under the ModelRoot and reparent a new
        # copy to it. This will remove all sub ModelRoot changes at the moment
        # and will need to be fixed in the future.
        # old_ids = {}
        import copy
        for comp in comps:
            index = comp.sibling_index
            print('index:', index)
            parent_np = comp.parent.data
            children = list(parent_np.get_children())
            print('num children:', len(children))
            for child in children:
                child.detach_node()

            print('pop:', children.pop(index))
            children.insert(index, copy.deepcopy(new_np))
            for child in children:
                child.reparent_to(parent_np)

        get_base().doc.on_modified()
