#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# interface_rigid.py
#
# This file is part of pymls, a software distributed under the MIT license.
# For any question, please contact one of the authors cited below.
#
# Copyright (c) 2019
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


def pem_rigid_interface(O):

    Omega_minus = np.zeros((6,3), dtype=np.complex)
    Omega_minus[2,0] = O[0]
    Omega_minus[4,0] = O[1]
    Omega_minus[0,1] = 1
    Omega_minus[3,2] = 1

    tau_tilde = 0

    return (Omega_minus, tau_tilde)


def elastic_rigid_interface(O):

    Omega_minus = np.zeros((4,2), dtype=np.complex)
    Omega_minus[1,0] = O[0]
    Omega_minus[2,0] = -O[1]
    Omega_minus[3,1] = 1

    tau_tilde = 0

    return (Omega_minus, tau_tilde)
