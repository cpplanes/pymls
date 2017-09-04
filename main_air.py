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

from pypw.transfert_layers import *
from pypw.transfert_interfaces import *
from pypw.pw_resolution import *
from pypw.initialize_omega_n_plus import *


freq = 1000
omega = 2*np.pi*freq

d = 0.05
theta = 23

k_0=omega*np.sqrt(Air.rho/Air.K)
k_x=k_0*np.sin(theta*np.pi/180)
Z_0=np.sqrt(Air.rho*Air.K)

# ========================
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
# ========================

Omega_moins = Initialize_Omega_n_plus()
(Omega_plus, Xi) = Transfert_Fluid(Omega_moins, omega, k_x, Air.K, Air.rho, d)
R_recursive_old = PW_Resolution(Omega_plus, omega, k_x, Air.K, Air.rho)


Z_s = -1j*Air.Z/np.tan(k_air*d)
R = (Z_s-Air.Z)/(Z_s+Air.Z)

print("R_recursive=")
print(R_recursive)
print("R_recursive_old=")
print(R_recursive_old)
print("R_analytique=")
print(R)

# PLANES_Reference=np.loadtxt('../../PLANES/Projects/pypw/out/pypw_101.PW')

plt.figure()
# plt.plot(PLANES_Reference[:,0],PLANES_Reference[:,2],'b')
# plt.plot(PLANES_Reference[:,0],PLANES_Reference[:,3],'r')
plt.plot(freq,R_recursive.real, 'b.')
plt.plot(freq,R_recursive.imag, 'r.')
plt.show()
