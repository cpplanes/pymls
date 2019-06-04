#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# transfert_interfaces.py
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


def fluid_pem_interface(O):

    a = -np.array([
        [O[0,1],O[0,2]],
        [O[3,1],O[3,2]]
    ])
    tau = np.dot(np.linalg.inv(a), np.array([[O[0,0]], [O[3,0]]]))
    tau_tilde = np.concatenate([np.eye(1),tau])

    Omega_minus = np.array([[O[2,0]], [O[4,0]]]) + np.dot(np.array([[O[2,1], O[2,2]], [O[4,1], O[4,2]]]), tau)

    return (Omega_minus, tau_tilde)


def pem_fluid_interface(O):

    Omega_minus = np.zeros((6,3), dtype=np.complex)
    Omega_minus[1,1] = 1
    Omega_minus[2,0] = O[0,0]
    Omega_minus[4,0] = O[1,0]
    Omega_minus[5,2] = 1

    tau_tilde = np.zeros((1,3), dtype=np.complex)
    tau_tilde[0,0] = 1

    return (Omega_minus, tau_tilde)


def elastic_fluid_interface(O):

    Omega_minus = np.zeros((4,2), dtype=np.complex)
    Omega_minus[1,0] = O[0,0]
    Omega_minus[2,0] = -O[1,0]
    Omega_minus[3,1] = 1

    tau_tilde = np.zeros((1,2), dtype=np.complex)
    tau_tilde[0,0] = 1

    return (Omega_minus, tau_tilde)


def fluid_elastic_interface(O):

    tau = -O[0,0]/O[0,1]
    Omega_minus = np.array([[O[1,1]], [-O[2,1]]])*tau + np.array([[O[1,0]], [-O[2,0]]])
    tau_tilde = np.concatenate([np.eye(1,1), np.array([[tau]])])

    return (Omega_minus, tau_tilde)


def pem_elastic_interface(O):

    Omega_minus = np.zeros((6,3), dtype=np.complex)
    Omega_minus[0,0:2] = O[0,0:2]
    Omega_minus[1,0:2] = O[1,0:2]
    Omega_minus[2,0:2] = O[1,0:2]
    Omega_minus[3,0:2] = O[2,0:2]
    Omega_minus[3,2] = 1
    Omega_minus[4,2] = 1
    Omega_minus[5,0:2] = O[3,0:2]

    tau_tilde = np.zeros((2,3), dtype=np.complex)
    tau_tilde[0,0] = 1
    tau_tilde[1,1] = 1
    return (Omega_minus, tau_tilde)


def elastic_pem_interface(O):

    Dplus = np.array([0, 1, -1, 0, 0, 0])
    Dminus = np.zeros((4,6), dtype=np.complex)
    Dminus[0,0] = 1
    Dminus[1,1] = 1
    Dminus[2,3] = 1
    Dminus[2,4] = -1
    Dminus[3,5] = 1
    tau = -Dplus.dot(O[:,2:4])**-1 * np.dot(Dplus, O[:,0:2])

    Omega_minus = Dminus.dot(O[:,0:2] + O[:,2:4]*tau)

    tau_tilde = np.vstack([np.eye(2), tau])

    return (Omega_minus, tau_tilde)
