#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# medium.py
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


class Medium(object):
    """ Holds a medium definition and allows its manipulation and loading """

    EXPECTED_PARAMS = []
    MEDIUM_TYPE = 'generic'

    def __init__(self):
        self.frequency = -1

    def update_frequency(self, freq):
        """ Computes parameters' value for the given frequency """
        pass

    def from_dict(self, parameters):
        """Reads medium definition from a hashmap of params.
        Raises a LookupError if the parameter definition is incomplete."""

        for param in self.__class__.EXPECTED_PARAMS:
            param_value = parameters.get(param)
            if param_value is None:
                raise LookupError(f'Unable to find definition of parameter "{param}"')
            else:
                setattr(self, param, param_value)
