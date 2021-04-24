import logging
import os

import panda3d.core as pc
from panda3d.core import Shader

from game.plugins import base


logger = logging.getLogger(__name__)


class HelpersPlugin(base.Base):

    def on_init(self, base):

        # Load vertex colour shader.
        vtx_shader = Shader.load(self.get_model_path('vertex_colours.sha'))

        # Set editor meshes.
        model_to_wrapper = {
            'camera.egg': 'BaseCam',
            'ambient_light.egg': 'AmbientLight',
            'spotlight.egg': 'Spotlight',
            'point_light.egg': 'PointLight',
            'directional_light.egg': 'DirectionalLight'
        }
        for model_name, wrpr_name in model_to_wrapper.items():
            model = base.loader.load_model(self.get_model_path(model_name))
            model.set_shader(vtx_shader)
            try:
                base.node_manager.wrappers[wrpr_name].set_editor_geometry(model)
            except KeyError:
                logger.error(
                    f'Could not set geometry on wrapper: {wrpr_name}. Perhaps '
                    f'it\'s not loaded?'
                )

    def get_model_path(self, file_name):
        """
        Return the model path for the specified file name. Model paths are
        given as absolute paths so there is no need to alter the model search
        path - doing so may give weird results if there is a similarly named
        model in the user's project.

        """
        dir_path = os.path.join(os.path.split(__file__)[0], 'data')
        model_path = pc.Filename.from_os_specific(os.path.join(dir_path, file_name))
        return model_path
