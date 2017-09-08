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

from matplotlib import pyplot as plt
import numpy as np

from pypw.media import Air
from pypw.solver import Solver
import pypw.backing as backing

freq = 1000
omega = 2*np.pi*freq

d = 0.05
theta = 0

k_air = omega*np.sqrt(Air.rho/Air.K)
k_x = k_air*np.sin(theta*np.pi/180)


S = Solver()
S.media = {'air': Air}
S.layers = [
    {
        'medium': 'air',
        'thickness': d,
    },
]
S.backing = backing.rigid

result = S.solve(freq, k_x)
R_recursive = result['R'][0]

Z_s = -1j*Air.Z/np.tan(k_air*d)
R = (Z_s-Air.Z)/(Z_s+Air.Z)

print("R_recursive=")
print(R_recursive)
print("R_analytique=")
print(R)

# PLANES_Reference=np.loadtxt('../../PLANES/Projects/pypw/out/pypw_101.PW')

# plt.figure()
# plt.plot(PLANES_Reference[:,0],PLANES_Reference[:,2],'b')
# plt.plot(PLANES_Reference[:,0],PLANES_Reference[:,3],'r')
# plt.plot(freq,R_recursive.real, 'b.')
# plt.plot(freq,R_recursive.imag, 'r.')
# plt.show()
