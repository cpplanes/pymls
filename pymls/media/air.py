#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# air.py
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

from .medium import Medium


class Air(Medium):

    MEDIUM_TYPE = 'fluid'
    MODEL = MEDIUM_TYPE

    T = 293.15  # reference temperature [K]
    P = 1.01325e5  # atmospheric Pressure [Pa]
    gamma = 1.400  # polytropic coefficient []
    lambda_ = 0.0262  # thermal conductivity [W.m^-1.K^-1]
    mu = 0.1839e-4  # dynamic viscosity [kg.m^-1.s^-1]
    Pr = 0.710  # Prandtl's number []
    molar_mass = 0.29e-1  # molar mass [kg.mol^-1]
    rho = 1.213  # density [kg.m^-3]
    C_p = 1006  # (mass) specific heat capacity as constant pressure [J.K^-1]

    K = gamma*P  # adiabatic bulk modulus
    c = np.sqrt(K/rho)  # adiabatic sound speed
    Z = rho*c  # characteristic impedance
    C_v = C_p/gamma  # (mass) specific heat capacity as constant volume [J.K^-1]
    nu = mu/rho  # kinematic viscosity [m.s^-2]
    nu_prime = nu/Pr  # viscothermal losses

    def from_yaml(self, *args, **kwargs):
        pass

    def update_frequency(self, *args, **kwargs):
        pass
