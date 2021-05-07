from game.nodes.attributes import PyTagProjectAssetAttribute


class ParticleEffect:

    serialise_descendants = False
    config_path = PyTagProjectAssetAttribute(
        required=True,
    )
