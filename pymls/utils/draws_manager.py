#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# draws_manager.py
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


class DrawsManager(object):
    """Encapsulates the handling of PDF for StochasticLayer"""

    def __init__(self, draws, mean, std):
        self.draws = draws
        self.N = len(draws)
        self.mean = mean
        self.std = std
        self.n = 0

    def as_pdf(self):
        if self.n == self.N:
            raise ValueError('The distribution has  only {} samples.'.format(self.N))
        else:
            val = self.mean+self.draws[self.n]*self.std
            self.n += 1
            return float(val)

    def reset(self):
        self.n = 0

    def __len__(self):
        return self.N
