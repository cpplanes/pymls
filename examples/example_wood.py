#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# main.py
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

import sys
sys.path.append('../')

from pymls import from_yaml, Solver, Layer, backing

freq = 10
theta = 5

bois = from_yaml('materials/wood.yaml')
d_bois = 2e-3

S = Solver()
S.layers = [Layer(bois, d_bois)]
S.backing = backing.rigid

result = S.solve(freq, theta)
pymls = result['R'][0]

print("pymls: R = ", pymls)
