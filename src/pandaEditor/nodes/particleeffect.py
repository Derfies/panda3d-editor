import panda3d.core as pc

from game.nodes.attributes import ProjectAssetPythonTagAttribute


class ParticleEffect:

    serialise_descendants = False
    config_path = ProjectAssetPythonTagAttribute(
        pc.Filename,
        read_only=True,
        required=True,
    )
