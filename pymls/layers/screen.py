#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# screen.py
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


def transfert_screen(Omega_moins, omega, k_x, m, d):

    # For reference: the full alpha matrix
    # alpha = np.array([
    #     [0, 0, 0, 1j*k_x*m.A_hat/m.P_hat, 1j*k_x*m.gamma_til, -(m.A_hat**2-m.P_hat**2)/m.P_hat*k_x**2-m.rho_til*omega**2],
    #     [0, 0, 0, 1/m.P_hat, 0, 1j*k_x*m.A_hat/m.P_hat],
    #     [0, 0, 0, 0, -1/m.K_eq_til+k_x**2/(m.rho_eq_til*omega**2), -1j*k_x*m.gamma_til],
    #     [1j*k_x, -m.rho_s_til*omega**2, -m.rho_eq_til*m.gamma_til*omega**2, 0, 0, 0],
    #     [0, m.rho_eq_til*m.gamma_til*omega**2, m.rho_eq_til*omega**2, 0, 0, 0],
    #     [1/m.N, 1j*k_x, 0, 0, 0, 0]
    # ])

    alpha = np.array([
        [0, 0, 0, 0, 0, -(m.A_hat**2-m.P_hat**2)/m.P_hat*k_x**2-m.rho_til*omega**2],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, -1/m.K_eq_til+k_x**2/(m.rho_eq_til*omega**2), 0],
        [0, -m.rho_s_til*omega**2, -m.rho_eq_til*m.gamma_til*omega**2, 0, 0, 0],
        [0, m.rho_eq_til*m.gamma_til*omega**2, m.rho_eq_til*omega**2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ])
    T = np.eye(6) - d*alpha

    Omega_plus = T @ Omega_moins
    Xi = np.eye(3)

    return (Omega_plus, Xi)
