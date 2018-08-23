#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# layer.py
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

import copy


class Layer(object):

    def __init__(self, medium, thickness, name="Unnamed Layer"):
        self.thickness = thickness
        self.medium = copy.deepcopy(medium)
        self.name = name
        self.hooks = {
            'pre_update_frequency': []
        }

    def update_frequency(self, omega):
        for f in self.hooks['pre_update_frequency']:
            f(self)
        self.medium.update_frequency(omega)

    def register(self, hook_name):
        if self.hooks.get(hook_name) is None:
            raise ValueError("Invalid hook name. Use one of : {}".format(','.join(self.hooks.keys())))

        def decorator(func):
            self.hooks[hook_name].append(func)
        return decorator

    def __str__(self):
        return '{} - {}m of {} ({})'.format(
            self.name,
            self.thickness,
            self.medium.name,
            self.medium.MEDIUM_TYPE
        )


class StochasticLayer(Layer):

    def __init__(self, medium, thickness, stochastic_param, pdf, name="Unnamed Layer"):
        """
        medium -- medium object
        thickness -- layer's thickness
        stochastic_param -- name of the stochastic parameter
        pdf -- probability density function from which are drawn the random samples
        name -- optional layer's name

        Please note that the pdf is a **function handle** that must return
        a sample per call (and accepts no argument)
        """

        super().__init__(medium, thickness, name)
        self.stochastic_param = stochastic_param
        self.pdf = pdf

        # useful for type lookup and guards
        self.__medium_params = dict(self.medium.EXPECTED_PARAMS+self.medium.OPT_PARAMS)

        if self.stochastic_param == 'thickness':
            setattr(self, 'new_draw', self.__draw_thickness)
            self.initial_param_value = self.thickness
        elif self.stochastic_param in self.__medium_params.keys():
            self.initial_param_value = getattr(self.medium, self.stochastic_param)
            setattr(self, 'new_draw', self.__draw_medium_parameter)
        else:
            raise ValueError('Unable to draw a parameter undefined in the layer')

    def __draw_thickness(self):
        draw = float(self.pdf())
        self.thickness = draw
        return draw

    def __draw_medium_parameter(self):
        draw = self.pdf()
        expected_type = self.__medium_params[self.stochastic_param]
        if type(draw) == expected_type:
            setattr(self.medium, self.stochastic_param, draw)
            self.medium.omega = -1
        else:
            raise TypeError('Draw of type {} but expected type {}'.format(
                type(draw),
                expected_type
            ))
        return draw

    def reinit(self):
        if self.stochastic_param == 'thickness':
            self.thickness = self.initial_param_value
        else:
            setattr(self.medium, self.stochastic_param, self.initial_param_value)
