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
from transfert_layers import *
from transfert_interfaces import *

omega=10
k_x=0 
K_air =1.418891313475211e+05
rho_air =1.204215082737155 
d=0.1

k_air=omega*np.sqrt(rho_air/K_air)
Z_air=np.sqrt(rho_air*K_air)



Omega_moins=np.array([[0],[1]])     

(Omega_plus,Xi)=  Transfert_Fluid(Omega_moins,omega,k_x,K_air,rho_air,d/2.0)


(Omega_plus_2,Xi)=Transfert_Fluid(Omega_plus,omega,k_x,K_air,rho_air,d/2.0)
print(Omega_plus_2[1]/(1j*omega*Omega_plus_2[0]))


print(-1j*Z_air/np.tan(k_air*d))

