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

import numpy as np

from pymls import Solver, Layer, backing
from pymls.media import Air

freq = 1000
omega = 2*np.pi*freq

d = 0.05
theta = 0

# Analytical solution
k_air = omega*np.sqrt(Air.rho/Air.K)
Z_s = -1j*Air.Z/np.tan(k_air*d)
R_analytical = (Z_s-Air.Z)/(Z_s+Air.Z)

# Solution using pymls
S = Solver()
S.layers = [Layer(Air, d)]
S.backing = backing.rigid

result = S.solve(freq, theta)
pymls = result[0]['R'][0]

print('Analytical : R = ', R_analytical)
print('pymls : R = ', pymls)
