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
from transfert_layers import *
from transfert_interfaces import *
from pw_resolution import *
from initialize_omega_n_moins import *

freq=1000
omega=2*np.pi*freq
 
K_0 =1.418891313475211e+05
rho_0 =1.204215082737155 
d=0.05


theta=23

k_0=omega*np.sqrt(rho_0/K_0)


k_x=k_0*np.sin(theta*np.pi/180)
Z_0=np.sqrt(rho_0*K_0)

Omega_moins=Initialize_Omega_n_moins()   

(Omega_plus,Xi)=  Transfert_Fluid(Omega_moins,omega,k_x,K_0,rho_0,d)

R_recursive=PW_Resolution(Omega_plus,omega,k_x,K_0,rho_0)

Z_s=-1j*Z_0/np.tan(k_0*d)
R=(Z_s-Z_0)/(Z_s+Z_0)

print("R_recursive=")
print(R_recursive)
print("R_analytique=")
print(R)

PLANES_Reference=np.loadtxt('../../PLANES/Projects/pypw/out/pypw_101.PW')

plt.figure()
plt.plot(PLANES_Reference[:,0],PLANES_Reference[:,2],'b')
plt.plot(PLANES_Reference[:,0],PLANES_Reference[:,3],'r')
plt.plot(freq,R_recursive.real,'b.')
plt.plot(freq,R_recursive.imag,'r.')
plt.show()

