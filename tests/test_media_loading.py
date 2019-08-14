#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# media_loading.py
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

import pytest
import tempfile
import os

from pymls.media import from_yaml, Air, EqFluidJCA
from pymls.media.medium import Medium


class TestMediaLoading:

    @pytest.fixture
    def yaml_fn(self, tmpdir):
        return tmpdir.join('medium.yaml')

    def test_file_not_found(self, tmpdir):

        with pytest.raises(IOError):
            from_yaml(tmpdir.join('inexistent.yaml'))

    def test_bad_medium_type(self, yaml_fn):
        with open(yaml_fn, 'w') as fh:
            fh.write('medium_type: phony_medium\n')

        with pytest.raises(ValueError):
            from_yaml(yaml_fn)

    def test_missing_parameter(self, yaml_fn):
        params = ['phi', 'sigma', 'alpha', 'Lambda_prime']

        with open(yaml_fn, 'w') as fh:
            fh.write('medium_type: eqf\n')
            for p in params:
                fh.write('{}: 42\n'.format(p))

        with pytest.raises(LookupError):
            from_yaml(yaml_fn)

    def test_ok_loading_eqf(self, yaml_fn):
        params = ['phi', 'sigma', 'alpha', 'Lambda_prime', 'Lambda',
                  'rho_1', 'nu', 'E', 'eta']

        with open(yaml_fn, 'w') as fh:
            fh.write('medium_type: eqf\n')
            for ii, p in enumerate(params):
                fh.write('{}: {}\n'.format(p, ii))

        medium = from_yaml(yaml_fn)
        for ii, p in enumerate(params):
            assert getattr(medium, p) == ii
