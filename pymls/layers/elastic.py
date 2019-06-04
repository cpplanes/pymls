#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# elastic.py
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


def transfert_elastic(Omega_minus, omega, k_x, medium, d):

    P_mat = medium.lambda_ + 2*medium.mu
    delta_p = omega*sqrt(medium.rho/P_mat)
    delta_s = omega*sqrt(medium.rho/medium.mu)

    beta_p = sqrt(delta_p**2-k_x**2)
    beta_s = sqrt(delta_s**2-k_x**2)

    alpha_p = -1j*medium.lambda_*delta_p**2 - 2j*medium.mu*beta_p**2
    alpha_s = 2j*medium.mu*beta_s*k_x

    Phi_0 = np.zeros((4,4),dtype=np.complex)
    Phi_0[0,0] = -2j*medium.mu*beta_p*k_x
    Phi_0[0,1] = 2j*medium.mu*beta_p*k_x
    Phi_0[0,2] = 1j*medium.mu*(beta_s**2-k_x**2)
    Phi_0[0,3] = 1j*medium.mu*(beta_s**2-k_x**2)

    Phi_0[1,0] = beta_p
    Phi_0[1,1] = -beta_p
    Phi_0[1,2] = k_x
    Phi_0[1,3] = k_x

    Phi_0[2,0] = alpha_p
    Phi_0[2,1] = alpha_p
    Phi_0[2,2] = -alpha_s
    Phi_0[2,3] = alpha_s

    Phi_0[3,0] = k_x
    Phi_0[3,1] = k_x
    Phi_0[3,2] = -beta_s
    Phi_0[3,3] = beta_s

    V_0 = np.array([
        1j*beta_p,
        -1j*beta_p,
        1j*beta_s,
        -1j*beta_s
    ])
    index = np.argsort(V_0.real)

    Phi = np.zeros((4,4), dtype=np.complex)
    lambda_ = np.zeros((4), dtype=np.complex)

    for i_m in range(0,4):
        Phi[:,i_m] = Phi_0[:,index[3-i_m]]
        lambda_[i_m] = V_0[index[3-i_m]]

    Phi_inv = np.linalg.inv(Phi)

    Lambda = np.diag([
        0,
        1,
        np.exp((lambda_[2]-lambda_[1])*d),
        np.exp((lambda_[3]-lambda_[1])*d)
    ])

    alpha_prime = Phi.dot(Lambda).dot(Phi_inv)

    xi_prime = Phi_inv[:1,:] @ Omega_minus
    xi_prime = np.concatenate([xi_prime, np.array([[0,1]])])  # TODO
    xi_prime_lambda = np.linalg.inv(xi_prime).dot(np.diag([
        np.exp((lambda_[1]-lambda_[0])*d),
        1
    ]))

    Omega_plus = alpha_prime.dot(Omega_minus).dot(xi_prime_lambda)
    Omega_plus[:,0] += Phi[:,0]

    Xi = xi_prime_lambda*np.exp(-lambda_[1]*d)

    return (Omega_plus, Xi)
