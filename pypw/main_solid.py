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

freq=10e6
omega=2*np.pi*freq

c_0=1480 
rho_0 =1000 
K_0 =rho_0*c_0**2

d=0.5e-3


lambda_verre =4.820087500000000e+10
mu_verre = 6.072612500000000e+10
rho_verre = 5000

theta=10

k_0=omega*np.sqrt(rho_0/K_0)

k_x=k_0*np.sin(theta*np.pi/180)
k_z=sqrt(k_0**2-k_x**2)

#print(k_x)
#print(k_z)

Z_0=np.sqrt(rho_0*K_0)


Omega_n_plus=np.array([[-1j*k_z/(rho_0*omega**2)],[1]]);
#print(Omega_n_plus)
Omega_n_moins=Interface_Solid_Fluid(Omega_n_plus)
#print(Omega_n_moins)

(Omega_1_plus,Xi_1)=Transfert_Elastic(Omega_n_moins,omega,k_x,lambda_verre,mu_verre,rho_verre,d)








