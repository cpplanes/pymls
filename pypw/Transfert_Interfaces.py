#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# Transfert_Interfaces.py
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


def Interface_Fluid_Pem(O):
   
#Tau=-inv([O(2,2) O(2,3);O(6,2) O(6,3)])*[O(2,1);O(6,1)];
#Omega_moins=[O(3,1);O(5,1)]+[O(3,2) O(3,3);O(5,2) O(5,3)]*Tau;       
    a=-np.array([O[1,1],O[1,2]],[O[5,1],O[5,2]]);
    Tau=np.dot(np.linalg.inv(a),np.array([[O[1,0]],[O[5,0]]]));
    Omega_moins=np.array([[O[2,0]],[O[4,0]]])+np.dot(np.array([[O[2,1],O[2,2]],[O[4,1],O[4,2]]]),Tau);
    return Tau, Omega_moins

def Interface_Fluid(O):
    return O