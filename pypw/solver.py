#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# solver.py
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
from numpy.lib.scimath import sqrt

from .interface.utils import generic_interface
from .layers.utils import generic_layer
import pypw.backing as backing
from .media import Air


class IncompleteDefinitionError(Exception):

    def __init__(self, msg='The definition is incomplete and no analysis can be performed'):
        super().__init__(msg)


class Solver(object):
    """
    Stores a system to solve and parameters for the analysis.
    Performs analysis and gives back raw unmodified/cleaned results.

    All post-processing should be done *out* of this class
    """

    def __init__(self, media=None, analysis=None, layers=None, backing=None):
        self.media = media
        self.analysis = analysis
        self.layers = layers
        self.backing = backing

    def is_complete(self):
        """ Checks that all the required data has been provided. """
        return True

    def solve(self, frequency=None, k_x=0):
        if not self.is_complete():
            raise IncompleteDefinitionError

        if frequency is None:
            for a in self.analysis:
                if a['type'] == 'frequency':
                    self.results.append(self.solve([a['value']], k_x))
                elif a['type'] == 'range':
                    frequencies = np.arange(a['start'], a['end'], a['step']).tolist()
                    self.results.append(self.solve(frequencies, k_x))

        elif type(frequency) != list:
            frequency = [frequency]

        result = {'f': [], 'R': [], 'T': []}
        for f in frequency:
            (R, T) = self.__solve_one_frequency(f, k_x)
            result['f'].append(f)
            result['R'].append(R)
            if T is not None:
                result['T'].append(T)

        if len(result['T']) == 0:
            del result['T']

        return result

    def __solve_one_frequency(self, frequency, k_x):

        omega = frequency*2*np.pi

        for m in self.media:
            self.media[m].update_frequency(omega)

        # load the backing vector to initiate recursion
        Omega_plus = self.backing(omega, k_x)

        # goes backward (from last to first layer) and compute successive
        # Omega_plus/minus
        back_prop = np.eye(1)
        for invertedi_L, L in enumerate(self.layers[::-1]):

            i_L = len(self.layers)-invertedi_L-1

            if invertedi_L == 0:  # right-most layer
                interface_func = generic_interface(self.media.get(L['medium']), Air)
            else:
                interface_func = generic_interface(self.media.get(L['medium']), self.media.get(self.layers[i_L+1]['medium']))

            if interface_func is not None:
                (Omega_moins, tau) = interface_func(Omega_plus)
            else:
                Omega_moins = Omega_plus
                tau = np.eye(len(Omega_moins))

            layer_func = generic_layer(self.media.get(L['medium']))
            (Omega_plus, xi) = layer_func(Omega_moins, omega, k_x, self.media.get(L['medium']), L['thickness'])

            if self.backing == backing.transmission:
                back_prop = back_prop.dot(tau).dot(xi)

        # last interface
        interface_func = generic_interface(self.media.get(self.layers[0]['medium']), Air)
        if interface_func is not None:
            (Omega_moins, tau) = interface_func(Omega_plus)
            
        else:
            Omega_moins = Omega_plus
            tau = np.eye(len(Omega_moins))

        if self.backing == backing.transmission:
            back_prop = back_prop.dot(tau)

        # Solve for the first layer
        k_air = omega*sqrt(Air.rho/Air.K)
        k_z = sqrt(k_air**2-k_x**2)
        u_z = 1j*k_z/(Air.rho*omega**2)

        Omega_0_fluid = np.matrix([
            [u_z],
            [1]
        ]);
        S_fluid=np.matrix([
            [-u_z],
            [1]
        ]);

        temp=np.array([
            [Omega_moins[0,0], -u_z],
            [Omega_moins[1,0], -1]
        ])

        X = np.linalg.inv(temp).dot(S_fluid)
        
        reflx_coefficient = X[1,0]
        X_0_moins = X[0,0]

        if self.backing == backing.transmission:
            trans_coefficient = back_prop*X_0_moins
        else:
            trans_coefficient = None

        return (reflx_coefficient, trans_coefficient)
