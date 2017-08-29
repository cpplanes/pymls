#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# Transfert_layers.py
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


def Transfert_Fluid(Omega_moins,omega,k_x,K_eq,rho_eq,d):
    delta=omega*np.sqrt(rho_eq/K_eq)
    lambda_=-np.sqrt(complex(k_x**2-delta**2,0))
    alpha=-1j*K_eq*delta**2;
    
    Phi=np.matrix([[-lambda_/(rho_eq*omega**2),lambda_/(rho_eq*omega**2)],[1,1]])
    #Phi=-alpha*Phi
    Psi=(rho_eq*omega**2/(2*lambda_))*np.matrix([[1,lambda_/(rho_eq*omega**2)],[-1,lambda_/(rho_eq*omega**2)]])
    #Psi=-Psi/alpha
    
    Omega_plus=Phi[:,0]+np.exp(-2*lambda_*d)*np.dot(np.dot(Phi[:,1],Psi[1,:]),Omega_moins)/np.dot(Psi[0,:],Omega_moins)
    
    Xi=np.exp(-lambda_*d)/np.dot(Psi[0,:],Omega_moins);
    
    return Omega_plus,Xi
