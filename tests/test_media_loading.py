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

import unittest
import tempfile
import os

from pymls.media import from_yaml, Air, EqFluidJCA
from pymls.media.medium import Medium


class MediaLoadingTests(unittest.TestCase):

    def setUp(self):
        self.yaml_file = tempfile.mkstemp()[1]

    def tearDown(self):
        os.remove(self.yaml_file)

    def test_file_not_found(self):

        with self.assertRaises(IOError):
            from_yaml(self.yaml_file+'_inexistent')

    def test_bad_medium_type(self):
        with open(self.yaml_file, 'w') as fh:
            fh.write('medium_type: phony_medium\n')

        with self.assertRaises(ValueError):
            from_yaml(self.yaml_file)

    def test_missing_parameter(self):
        params = ['phi', 'sigma', 'alpha', 'Lambda_prime', 'Lambda',
                  'rho_1', 'nu', 'E']

        with open(self.yaml_file, 'w') as fh:
            fh.write('medium_type: eqf\n')
            for p in params:
                fh.write('{}: 42\n'.format(p))

        with self.assertRaises(LookupError):
            from_yaml(self.yaml_file)

    def test_ok_loading_eqf(self):
        params = ['phi', 'sigma', 'alpha', 'Lambda_prime', 'Lambda',
                  'rho_1', 'nu', 'E', 'eta']

        with open(self.yaml_file, 'w') as fh:
            fh.write('medium_type: eqf\n')
            for ii, p in enumerate(params):
                fh.write('{}: {}\n'.format(p, ii))

        medium = from_yaml(self.yaml_file)
        for ii, p in enumerate(params):
            self.assertEqual(getattr(medium, p), ii)
