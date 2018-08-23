#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# analysis.py
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

import re
import itertools

import numpy as np


RANGE_MATCHER = re.compile(r'^(\d+\.?\d*):(\d+\.?\d*)?:(\d+\.?\d*)$')


class Analysis:

    def __init__(self, name, freqs, angles, enable_stochastic=False):
        self.name = name
        self.freqs = self.__parse_arg(freqs)
        self.angles = self.__parse_arg(angles)
        self.raw_freqs = freqs
        self.raw_angles = angles
        self.enable_stochastic = enable_stochastic

    def __parse_arg(self, arg):

        arg_t = type(arg)

        if arg_t == list:
            return np.array(arg)

        elif arg_t == str:
            matched_range = RANGE_MATCHER.match(arg)
            if matched_range is not None:
                (start, step, end) = matched_range.groups()
                try:
                    start, end = float(start), float(end)
                    step = float(step) if step is not None else None

                    return np.arange(start, end+step/2, step)
                except ValueError:
                    raise ValueError('Invalid literal definition (tried range): {}'.format(arg))
            else:
                try:
                    arg = float(arg)
                except ValueError:
                    try:
                        return np.array(list(map(float, filter(None, map(lambda _: _.strip(), arg.split(','))))))
                    except ValueError:
                        raise ValueError('Invalid literal definition (tried list): {}'.format(arg))
        else:
            try:
                return np.array([np.complex128(arg)])
            except TypeError:
                raise ValueError('Invalid literal definition (tried list): {}'.format(arg))

    def __iter__(self):
        return itertools.product(self.freqs, self.angles)
