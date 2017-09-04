#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# pw_resolution.py
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
from numpy.lib.scimath import *

# Function which return the reflexion coefficient at the incident interface

def PW_Resolution(Omega_moins,omega,k_x,K_0,rho_0):
    
    
    k_0=omega*sqrt(rho_0/K_0)
    k_z=sqrt(k_0**2-k_x**2)
    u_z=1j*k_z/(rho_0*omega**2)
    
    Omega_0_fluid=np.matrix([[u_z],[1]]);
    S_fluid=np.matrix([[-u_z],[1]]);
    
    
    temp=np.array([[Omega_moins[0,0],-u_z],[Omega_moins[1,0],-1]])
    
    print("temp=")
    print(temp)
    
    X=np.linalg.inv(temp).dot(S_fluid)
    return X