import logging
import json
import os

import numpy as np
import panda3d.core as pc
import wx
from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.attributes import PythonTagAttribute
from game.nodes.constants import TAG_NODE_TYPE
from game.nodes.nodepath import NodePath
from pandaEditor.plugins import base
from reactor.wfc.adjacencywavefunction import AdjacencyWaveFunction
from wxExtra import ActionItem


logger = logging.getLogger(__name__)


ID_CREATE_WFC = wx.NewId()


class WavefunctionCollapse(NodePath):

    type_ = pc.PandaNode
    shape_x = PythonTagAttribute(int, required=True)
    shape_y = PythonTagAttribute(int, required=True)
    shape_z = PythonTagAttribute(int, required=True)
    compatibilities_x = PythonTagAttribute(str)
    compatibilities_y = PythonTagAttribute(str)
    compatibilities_z = PythonTagAttribute(str)
    weights = PythonTagAttribute(str)
    sizes = PythonTagAttribute(str)

    # TODO: Need to figure out how to split game / editor plugins.
    @classmethod
    def get_default_values(cls):
        default_values = super().get_default_values()
        default_values.update({
            'shape_x': 1,
            'shape_y': 1,
            'shape_z': 1,
        })
        return default_values

    @classmethod
    def create(cls, *args, **kwargs):
        # Programatically do these?
        shape_x = kwargs.pop('shape_x')
        shape_y = kwargs.pop('shape_y')
        shape_z = kwargs.pop('shape_z')
        comp = super().create(cls, *args, **kwargs)
        comp.data.set_tag(TAG_NODE_TYPE, 'WavefunctionCollapse')    # Add to base nodepath?
        comp.shape_x = shape_x
        comp.shape_y = shape_y
        comp.shape_z = shape_z
        return comp


class WavefunctionCollapsePlugin(base.Base):

    def on_init(self):
        get_base().node_manager.wrappers['WavefunctionCollapse'] = WavefunctionCollapse

    def on_build_ui(self):
        camActns = [
            ActionItem('Collapse Wavefunction Node', '', self.on_collapse_node, ID_CREATE_WFC),
            ActionItem('Wavefunction Collapse Node', '', get_base().frame.on_create, args='WavefunctionCollapse'),
        ]
        get_base().frame.mCreate.AppendSeparator()
        get_base().frame.mCreate.AppendActionItems(camActns, get_base().frame)

    def on_update(self, comps):
        enabled = len(get_base().selection.comps) and all([
            isinstance(comp, WavefunctionCollapse)
            for comp in get_base().selection.comps
        ])
        get_base().frame.mCreate.Enable(ID_CREATE_WFC, enabled)

    def on_collapse_node(self, evt):

        # Do reverse compats automatically?
        # compatibilities = {
        #     (1, 0, 0): {
        #         ('empty', 'empty'),
        #         ('straight_x', 'straight_x'),
        #         ('empty', 'straight_y'),
        #         ('straight_y', 'empty'),
        #
        #         # Corners
        #         ('corner_-x-y', 'empty'),
        #         ('straight_x', 'corner_-x-y'),
        #
        #         ('corner_-xy', 'empty'),
        #         ('straight_x', 'corner_-xy'),
        #
        #         ('corner_x-y', 'straight_x'),
        #         ('empty', 'corner_x-y'),
        #
        #         ('corner_xy', 'straight_x'),
        #         ('empty', 'corner_xy'),
        #
        #         # Tees
        #         ('tee_-x', 'empty'),
        #         ('straight_x', 'tee_-x'),
        #         ('corner_x-y', 'tee_-x'),
        #         ('corner_xy', 'tee_-x'),
        #
        #         ('empty', 'tee_x'),
        #         ('tee_x', 'straight_x'),
        #         ('tee_x', 'corner_-xy'),
        #         ('tee_x', 'corner_-x-y'),
        #
        #
        #
        #         ('tee_-y', 'straight_x'),
        #         ('straight_x', 'tee_-y'),
        #         ('tee_-y', 'corner_-xy'),
        #         ('tee_-y', 'corner_-x-y'),
        #         ('corner_xy', 'tee_-y'),
        #         ('corner_x-y', 'tee_-y'),
        #
        #         ('tee_y', 'straight_x'),
        #         ('straight_x', 'tee_y'),
        #         ('tee_y', 'corner_-x-y'),
        #         ('tee_y', 'corner_-xy'),
        #         # ('corner_-xy', 'tee_y'),
        #         # ('corner_-x-y', 'tee_y'),
        #
        #         # Cross
        #         ('cross', 'cross'),
        #         ('cross', 'straight_x'),
        #         ('straight_x', 'cross'),
        #         ('cross', 'corner_-xy'),
        #         ('cross', 'corner_-x-y'),
        #         ('corner_xy', 'cross'),
        #         ('corner_x-y', 'cross'),
        #         ('cross', 'tee_-x'),
        #         ('cross', 'tee_y'),
        #         ('cross', 'tee_-y'),
        #         ('tee_x', 'cross'),
        #         ('tee_y', 'cross'),
        #         ('tee_-y', 'cross'),
        #
        #         # ('straight_x', 'corner_-xy'),
        #         # ('corner_-xy', 'empty'),
        #     },
        #
        #     (0, 1, 0): {
        #         ('empty', 'empty'),
        #         ('straight_y', 'straight_y'),
        #         ('straight_x', 'empty'),
        #         ('empty', 'straight_x'),
        #
        #         # Corners
        #         ('corner_-x-y', 'empty'),
        #         ('straight_y', 'corner_-x-y'),
        #
        #         ('corner_-xy', 'straight_y'),
        #         ('empty', 'corner_-xy'),
        #
        #         ('straight_y', 'corner_x-y'),
        #         ('corner_x-y', 'empty'),
        #
        #         ('corner_xy', 'straight_y'),
        #         ('empty', 'corner_xy'),
        #
        #         # Tees
        #         ('tee_-x', 'straight_y'),
        #         ('straight_y', 'tee_-x'),
        #         ('tee_-x', 'corner_x-y'),
        #         ('tee_-x', 'corner_-x-y'),
        #         ('corner_xy', 'tee_-x'),
        #         ('corner_-xy', 'tee_-x'),
        #
        #         ('tee_x', 'straight_y'),
        #         ('straight_y', 'tee_x'),
        #         ('tee_x', 'corner_x-y'),
        #         ('tee_x', 'corner_-x-y'),
        #         ('corner_xy', 'tee_x'),
        #         ('corner_-xy', 'tee_x'),
        #
        #
        #
        #         ('tee_-y', 'empty'),
        #         ('straight_y', 'tee_-y'),
        #         ('corner_xy', 'tee_-y'),
        #         ('corner_-xy', 'tee_-y'),
        #
        #         ('empty', 'tee_y'),
        #         ('tee_y', 'straight_y'),
        #         ('tee_y', 'corner_-x-y'),
        #         ('tee_y', 'corner_x-y'),
        #
        #
        #         # Cross
        #         ('cross', 'cross'),
        #         ('cross', 'straight_y'),
        #         ('straight_y', 'cross'),
        #         ('cross', 'corner_x-y'),
        #         ('cross', 'corner_-x-y'),
        #         ('corner_xy', 'cross'),
        #         ('corner_-xy', 'cross'),
        #         ('cross', 'tee_-y'),
        #         ('cross', 'tee_x'),
        #         ('cross', 'tee_-x'),
        #         ('tee_y', 'cross'),
        #         ('tee_x', 'cross'),
        #         ('tee_-x', 'cross'),
        #
        #
        #
        #         # ('straight_y', 'corner_-x-y'),
        #         # ('corner_xy', 'straight_y'),
        #         # ('corner_x-y', 'empty'),
        #     },
        # }

        comp = get_base().selection.comps[0]
        for nodepath in comp.data.get_children():
            nodepath.detach_node()

        compatibilities = {}
        for d, attr_name in {
            (1, 0, 0): 'compatibilities_x',
            (0, 1, 0): 'compatibilities_y',
            (0, 0, 1): 'compatibilities_z',
        }.items():
            value = getattr(comp, attr_name)
            if not value:
                continue
            compat_path = os.path.join(get_base().project.path, value)
            if not os.path.exists(compat_path):
                continue
            with open(compat_path) as json_file:
                compats = json.load(json_file)
                compatibilities[d] = compats

        # weights_path = os.path.join(get_base().project.path, comp.weights)
        # with open(weights_path) as json_file:
        #     weights = json.load(json_file)
        # print(weights)
        #print('compatibilities:', compatibilities)

        new_compatibilities = {}
        for d, compats in compatibilities.items():
            # print(d)
            # for c in compats:
            #     print('   ', c)
            new_compatibilities[d] = compats
            if d == (1, 0, 0):
                rev_d = (-1, 0, 0)
            elif d == (0, 1, 0):
                rev_d = (0, -1, 0)
            else:
                rev_d = (0, 0, -1)
                # rev_d = (-1, 0, 0) if d == (1, 0, 0) else (0, -1, 0)
            rev_compats = [(b, a) for (a, b) in compats]
            new_compatibilities[rev_d] = rev_compats


        shape = (comp.shape_x, comp.shape_y, comp.shape_z)

        weights_path = os.path.join(get_base().project.path, comp.weights)
        with open(weights_path) as json_file:
            weights = json.load(json_file)
        #print(weights)
        # weights = {
        #     'empty': 0.1,
        #     'corner_x-y': 0.1,
        #     'corner_-xy': 0.1,
        #     'corner_-x-y': 0.1,
        #     'corner_xy': 0.1,
        #     'straight_x': 2,
        #     'straight_y': 2,
        #     'tee_x': 0.1,
        #     'tee_-x': 0.1,
        #     'tee_y': 0.1,
        #     'tee_-y': 0.1,
        #     'cross': 0.1,
        # }
        wf = AdjacencyWaveFunction(new_compatibilities, shape, weights)
        wf.run()
        #print(get_colour_output(wf.wave, TILE_COLOURS, wf.tiles))

        # TODO: Add this as method to wave class.
        reshaped = wf.wave.reshape(wf.wave.shape[0], -1)
        chars = []
        for index in range(reshaped.shape[1]):
            states = reshaped[(slice(None), index)]
            tile = wf.tiles[np.argmax(states)]
            chars.append(tile)
        shaped = np.array(chars).reshape(*wf.wave.shape[1:])

        #size = 3

        sizes_path = os.path.join(get_base().project.path, comp.sizes)
        with open(sizes_path) as json_file:
            sizes = json.load(json_file)
        print(sizes)

        root_comp = get_base().node_manager.wrap(get_base().render)
        x_offset = 0
        for x, row in enumerate(shaped):
            y_offset = 0
            for y, col in enumerate(shaped[x]):
                z_offset = 0
                for z, stack in enumerate(shaped[x][y]):
                    model_name = shaped[x][y][z]
                    path = os.path.join(get_base().project.prefabs_directory, model_name)
                    model_path = pc.Filename.from_os_specific(path) + '.xml'
                    model = get_base().scene_parser.load(model_path, root_comp)
                    model.data.set_x(x_offset)
                    model.data.set_y(y_offset)
                    model.data.set_z(z_offset)
                    model.parent = comp
                    z_offset += sizes[model_name][2]
                y_offset += sizes[model_name][1]
            x_offset += sizes[model_name][0]

        get_base().doc.on_modified([])
