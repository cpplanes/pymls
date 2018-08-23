#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# yaml_loader.py
#
# This file is part of pymls, a software distributed under the MIT license.
# For any question, please contact one of the authors cited below.
#
# Copyright (c) 2017
# 	Olivier Dazel <olivier.dazel@univ-lemans.fr>
# 	Mathieu Gaborit <gaborit@kth.se>
# 	Peter Göransson <pege@kth.se>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#

import yaml

from ..media import from_yaml
from ..solver import Solver
from pymls.backing import rigid, transmission


class YamlLoader(object):
    """ Load a multilayer definition from a yaml file """

    EXPECTED_FIELDS = {
        'materials': {
            'type': [dict, dict],
            'item_keys': ['source'],
        },
        'multilayer': {
            'type': [list, dict],
            'item_keys': ['medium', 'thickness']
        },
        'analysis': {
            'type': [list, dict],
            'item_keys': ['type', 'values', 'start', 'end', 'step'],
        },
        'backing': {
            'type': [str]
        }
    }

    KEYS_ANALYSIS = {
        'frequency': ['type', 'value'],
        'range': ['type', 'start', 'end', 'step'],
    }

    MAP_BACKING = {
        'rigid': rigid,
        'transmission': transmission
    }

    def __init__(self):
        self.loaded_yaml = None

    def from_file(self, filename):
        with open(filename) as fh:
            self.loaded_yaml = yaml.load(fh)

        self.extract_from_yaml()

    def extract_from_yaml(self, yaml=None):
        if yaml is not None:
            self.yaml = yaml
        else:
            if self.yaml is None:
                raise ValueError("Empty yaml or no yaml given")

        if self.yaml_is_valid():
            self.parse_yaml()
        else:
            raise ValueError('Provided yaml does not comply with expected format')

    def yaml_is_valid(self):
        expected_keys = set(self.__class__.EXPECTED_FIELDS.keys())
        yaml_keys = set(self.loaded_yaml.keys())
        if not expected_keys == yaml_keys:
            raise ValueError('Invalid set of keys in definitions')

        for primary_k, primary_v in self.loaded_yaml.items():
            if not type(primary_v) == self.__class__.EXPECTED_FIELDS[primary_k]['type'][0]:
                raise ValueError('Invalid data type in definition of {}'.format(primary_k))
            if type(primary_v) == str:
                continue

            get = lambda _: primary_v.get(_) if self.__class__.EXPECTED_FIELDS[primary_k]['type'][0] == dict else lambda _: _  # noqa: E731
            for item in primary_v:
                if not type(get(item)) == self.__class__.EXPECTED_FIELDS[primary_k]['type'][1]:
                    raise ValueError('Invalid data type in definition of {}'.format(primary_k))

                expected_keys = set(self.__class__.EXPECTED_FIELDS[primary_k]['item_keys'])
                yaml_keys = set(get(item).keys())
                if not yaml_keys-expected_keys == set():
                    raise ValueError('Invalid set of keys in definitions')

        return True

    def parse_yaml(self):

        solver = Solver()

        # parse materials  TODO: try/except
        for m, def_ in self.loaded_yaml['materials'].items():
            medium = from_yaml(def_['source'])
            solver.media[m] = medium
            solver.media_keys.append(medium)

        # parse layers
        for i_l, l in enumerate(self.loaded_yaml['multilayer']):

            # Check that layer's definition is correct
            msg = 'Bad layer definition in layer {}'.format(i_l)
            error = False
            if l.get('thickness') < 0:
                msg += "thickness must be >= 0"
                error = True
            if l['medium'] not in solver.media_keys:
                if error:
                    msg += " & "
                msg += "media not found"
                error = True

            if error:
                raise ValueError(msg)
            else:
                solver.layers.append(l)

        # parse backing specification
        backing_func = self.__class__.MAP_BACKING.get(self.loaded_yaml['backing'])
        if backing_func is None:
            raise ValueError('Unknown backing type {}'.format(self.loaded_yaml['backing']))
        else:
            solver.backing = backing_func

        # parse analysis definitions
        for i_a, a in enumerate(self.loaded_yaml['analysis']):
            # check for a valid set of keys
            for typ, expected_keys in self.__class__.KEYS_ANALYSIS:
                if a['type'] == typ and set(a.keys) != set(expected_keys):
                    raise ValueError('Bad analysis definition for analysis {}'.format(i_a))
                else:
                    solver.analysis.append(a)
