#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# backing.py
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
from mediapack import Air


def rigid(omega, k_x):

    return np.array([
        [0],
        [1]
    ], dtype=np.complex128)


def transmission(omega, k_x):
    k_air = omega/Air.c
    k_z = sqrt(k_air**2-k_x**2)
    return np.array([
        [-1j*k_z/(Air.rho*omega**2)],
        [1]
    ], dtype=np.complex128)
