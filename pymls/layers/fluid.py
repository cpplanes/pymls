#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# fluid.py
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

import numpy as np
from numpy.lib.scimath import sqrt


def transfert_fluid(Omega_minus, omega, k_x, medium, d):

    if medium.MEDIUM_TYPE == 'eqf':
        rho = medium.rho_eq_til
        c = medium.c_eq_til
    elif medium.MEDIUM_TYPE == 'fluid':
        rho = medium.rho
        c = medium.c
    else:
        raise ValueError('Provided material is not a fluid')

    delta = omega/c

    # Eigenvalue of the State Matrix (the other one is -lambda_)
    lambda_ = -sqrt(k_x**2-delta**2)

    # Matrix of eigenvectors , Eq (A10) in JAP 2013 corrected
    Phi = np.array([
        [-lambda_/(rho*omega**2), lambda_/(rho*omega**2)],
        [1, 1]
    ], dtype=np.complex)

    # Analytical inverse of Phi
    Psi = (rho*omega**2/(2*lambda_))*np.array([
        [-1, lambda_/(rho*omega**2)],
        [1, lambda_/(rho*omega**2)]
    ], dtype=np.complex)

    Omega_plus = Phi[:,0].reshape(2,1) + np.exp(-2*lambda_*d) * (Phi[:,1].reshape(2,1) @ Psi[1,:].reshape(1,2)).dot(Omega_minus) / (Psi[0,:].reshape(1,2) @ Omega_minus)

    Xi = np.exp(-lambda_*d)/Psi[0,:].reshape(1,2).dot(Omega_minus)

    return (Omega_plus, Xi)
