#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# main_pem.py
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

import sys
sys.path.append('../')

import numpy as np
from pymls import from_yaml, Solver, StochasticLayer, backing

freqs = '20:10:2500'
d = 5e-2
theta = 30
n_draws = 20

foam = from_yaml('materials/foam2.yaml')

# define a function to draw samples
def pdf():
    return np.random.normal(d, d*.1)


# run the analysis
S = Solver()
S.layers = [ StochasticLayer(foam, d, 'thickness', pdf)]
S.backing = backing.rigid

result = S.solve(freqs, theta, n_draws=n_draws)


# produce a figure for the absorption coefficient
values = 1-abs(np.array(result['R']))**2

import matplotlib.pyplot as plt
plt.figure()
for i in range(len(result['stochastics']['values'])):
    plt.plot(result['f'], values[:,i], color='b', alpha=0.05)

# build and plot a mean
mean = np.mean(values, axis=1)
plt.plot(result['f'], mean, color='r', label='mean')

plt.xlabel('Frequency (Hz)')
plt.ylabel('Absorption Coefficient')
plt.legend()

plt.show()

