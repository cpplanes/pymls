#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# main.py
#
# This file is part of pypw, a software distributed under the MIT license.
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

import numpy as np

from pypw.media import from_yaml, Air
from pypw.solver import Solver
import pypw.backing as backing


freq = 10
omega = 2*np.pi*freq
d = 0.5e-3
theta = 10

glass = from_yaml('materials/verre.yaml')

k_air = omega*np.sqrt(Air.rho/Air.K)
k_x = k_air*np.sin(theta*np.pi/180)

S = Solver()
S.media = {
    'air': Air,
    'glass': glass,
}
S.layers = [
    {
        'medium': 'glass',
        'thickness': d,
    },
]
S.backing = backing.transmission

result = S.solve([freq], k_x)
R_recursive = result['R'][0]

print("R_recursive=")
print(R_recursive)
