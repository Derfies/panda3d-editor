import os

from direct.particles.ParticleEffect import ParticleEffect as DirectParticleEffect
from direct.showbase.PythonUtil import getBase as get_base
import panda3d.core as pc

from game.nodes.attributes import PyTagAttribute
from game.nodes.constants import TAG_NODE_TYPE
from game.nodes.nodepath import NodePath


class ParticleEffect(NodePath):

    type_ = DirectParticleEffect
    config_path = PyTagAttribute(str, init_arg='', pytag_name='particle_effect_config_path')

    @classmethod
    def create(cls, *args, **kwargs):
        get_base().enable_particles()

        effect = DirectParticleEffect()
        effect.set_tag(TAG_NODE_TYPE, 'ParticleEffect')

        file_path = kwargs.get('config_path')
        if file_path is not None:
            # HAXXOR
            # Make relative to project somehow. We don't get this problem with
            # models because of panda's model search path.
            if not os.path.isabs(file_path):
                file_path = os.path.join(get_base().project.path, file_path)
            file_path = os.path.normpath(file_path)  # .replace('\\', '/')
            file_path = pc.Filename.from_os_specific(file_path)

            effect.load_config(file_path)
            effect.start()

        comp = super().create(data=effect)
        if file_path is not None:
            comp.config_path.set(file_path)

        return comp
