#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# pem.py
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


def transfert_pem(Omega_moins, omega, k_x, medium, d):

    beta_1 = sqrt(medium.delta_1**2-k_x**2)
    beta_2 = sqrt(medium.delta_2**2-k_x**2)
    beta_3 = sqrt(medium.delta_3**2-k_x**2)
    alpha_1 = -1j*medium.A_hat*medium.delta_1**2 - 2j*medium.N*beta_1**2
    alpha_2 = -1j*medium.A_hat*medium.delta_2**2 - 2j*medium.N*beta_2**2
    alpha_3 = 2j*medium.N*beta_3*k_x

    Phi_0 = np.zeros((6,6), dtype=np.complex)
    Phi_0[0,0] = -2j*medium.N*beta_1*k_x
    Phi_0[0,1] = 2j*medium.N*beta_1*k_x
    Phi_0[0,2] = -2j*medium.N*beta_2*k_x
    Phi_0[0,3] = 2j*medium.N*beta_2*k_x
    Phi_0[0,4] = 1j*medium.N*(beta_3**2-k_x**2)
    Phi_0[0,5] = 1j*medium.N*(beta_3**2-k_x**2)

    Phi_0[1,0] = beta_1
    Phi_0[1,1] = -beta_1
    Phi_0[1,2] = beta_2
    Phi_0[1,3] = -beta_2
    Phi_0[1,4] = k_x
    Phi_0[1,5] = k_x

    Phi_0[2,0] = medium.mu_1*beta_1
    Phi_0[2,1] = -medium.mu_1*beta_1
    Phi_0[2,2] = medium.mu_2*beta_2
    Phi_0[2,3] = -medium.mu_2*beta_2
    Phi_0[2,4] = medium.mu_3*k_x
    Phi_0[2,5] = medium.mu_3*k_x

    Phi_0[3,0] = alpha_1
    Phi_0[3,1] = alpha_1
    Phi_0[3,2] = alpha_2
    Phi_0[3,3] = alpha_2
    Phi_0[3,4] = -alpha_3
    Phi_0[3,5] = alpha_3

    Phi_0[4,0] = 1j*medium.delta_1**2*medium.K_eq_til*medium.mu_1
    Phi_0[4,1] = 1j*medium.delta_1**2*medium.K_eq_til*medium.mu_1
    Phi_0[4,2] = 1j*medium.delta_2**2*medium.K_eq_til*medium.mu_2
    Phi_0[4,3] = 1j*medium.delta_2**2*medium.K_eq_til*medium.mu_2
    Phi_0[4,4] = 0
    Phi_0[4,5] = 0

    Phi_0[5,0] = k_x
    Phi_0[5,1] = k_x
    Phi_0[5,2] = k_x
    Phi_0[5,3] = k_x
    Phi_0[5,4] = -beta_3
    Phi_0[5,5] = beta_3

    V_0 = np.array([
        1j*beta_1,
        -1j*beta_1,
        1j*beta_2,
        -1j*beta_2,
        1j*beta_3,
        -1j*beta_3
    ])

    # reverse sort
    index = np.argsort(V_0.real)
    index = index[::-1]

    # sorted versions
    Phi = Phi_0[:,index]
    lambda_ = V_0[index]

    Phi_inv = np.linalg.inv(Phi)

    Lambda = np.diag([
        0,
        0,
        1,
        np.exp((lambda_[3]-lambda_[2])*d),
        np.exp((lambda_[4]-lambda_[2])*d),
        np.exp((lambda_[5]-lambda_[2])*d)
    ])

    alpha_prime = Phi.dot(Lambda).dot(Phi_inv)

    xi_prime = Phi_inv[:2,:] @ Omega_moins
    xi_prime = np.concatenate([xi_prime, np.array([[0,0,1]])])  # TODO
    xi_prime_lambda = np.linalg.inv(xi_prime).dot(np.diag([
        np.exp((lambda_[2]-lambda_[0])*d),
        np.exp((lambda_[2]-lambda_[1])*d),
        1
    ]))

    Omega_plus = alpha_prime.dot(Omega_moins).dot(xi_prime_lambda)
    Omega_plus[:,0] += Phi[:,0]
    Omega_plus[:,1] += Phi[:,1]

    # eq. 24
    Xi = xi_prime_lambda*np.exp(-lambda_[2]*d)

    return (Omega_plus, Xi)
