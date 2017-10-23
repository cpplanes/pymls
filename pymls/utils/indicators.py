#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# indicators.py
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


def alpha_from_R(R):
    """ Compute the absorption coefficient from the Reflexion coefficient """
    return 1-np.abs(R)**2


def TL_from_T(T):
    """ Compute the Transmission Loss from the Transmission coefficient """
    return -20*np.log10(np.abs(T))
