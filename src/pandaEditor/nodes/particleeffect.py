from game.nodes.attributes import PyTagProjectAssetAttribute


class ParticleEffect:

    serialise_descendants = False
    config_path = PyTagProjectAssetAttribute(
        str,
        required=True,
        pytag_name='particle_effect_config_path',
    )
