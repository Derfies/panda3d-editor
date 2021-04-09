from pandac.PandaModules import Vec3


P3D_VERSION = '0.1'


__version__ = P3D_VERSION


from .constants import *
from .functions import *
from . import commonUtils

from .object import Object
from .singleTask import SingleTask
from .nodePathObject import NodePathObject
from .pandaObject import *
from .pandaBehaviour import PandaBehaviour
from .pandaManager import PandaManager

from .marquee import Marquee
from .camera import *
from .editorCamera import EditorCamera
from .frameRate import FrameRate
from .displayShading import DisplayShading
from .mouse import *
from .mousePicker import MousePicker
from . import geometry
try:
    import wxPanda as wx
except:
    print('Failed to find wx module')