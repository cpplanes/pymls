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

from pymls.media import from_yaml, Air, EqFluidJCA, Fluid, PEM, Elastic
from pymls.media.medium import Medium


class TestMediaLoading:

    @pytest.fixture
    def yaml_fn(self, tmpdir):
        path =  tmpdir.join('medium.yaml')
        path.ensure()
        return path.strpath

    def test_file_not_found(self, tmpdir):

        with pytest.raises(IOError):
            from_yaml(tmpdir.join('inexistent.yaml').strpath)

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

    def test_ok_loading_eqf_withoutopts(self, yaml_fn):
        params = ['phi', 'sigma', 'alpha', 'Lambda_prime', 'Lambda']

        with open(yaml_fn, 'w') as fh:
            fh.write('medium_type: eqf\n')
            for ii, p in enumerate(params):
                fh.write('{}: {}\n'.format(p, ii))

        medium = from_yaml(yaml_fn)
        for ii, p in enumerate(params):
            assert getattr(medium, p) == ii


    def test_ok_loading_eqf_withopts(self, yaml_fn):
        params = ['phi', 'sigma', 'alpha', 'Lambda_prime', 'Lambda',
                  'rho_1', 'nu', 'E', 'eta']

        with open(yaml_fn, 'w') as fh:
            fh.write('medium_type: eqf\n')
            for ii, p in enumerate(params):
                fh.write('{}: {}\n'.format(p, ii))

        medium = from_yaml(yaml_fn)
        for ii, p in enumerate(params):
            assert getattr(medium, p) == ii

    def test_ok_loading_fluid(self, yaml_fn):
        params = ['rho', 'c']

        with open(yaml_fn, 'w') as fh:
            fh.write('medium_type: fluid\n')
            for ii, p in enumerate(params):
                fh.write('{}: {}\n'.format(p, ii))

        medium = from_yaml(yaml_fn)
        for ii, p in enumerate(params):
            assert getattr(medium, p) == ii

    def test_ok_loading_pem(self, yaml_fn):
        params = ['phi', 'sigma', 'alpha', 'Lambda_prime', 'Lambda', 'rho_1', 'nu', 'E',
                  'eta', 'loss_type']

        with open(yaml_fn, 'w') as fh:
            fh.write('medium_type: pem\n')
            for ii, p in enumerate(params):
                if p!='loss_type':
                    fh.write('{}: {}\n'.format(p, ii))
                else:
                    fh.write('{}: structural\n'.format(p))

        medium = from_yaml(yaml_fn)
        for ii, p in enumerate(params):
            if p!='loss_type':
                assert getattr(medium, p) == ii
            else:
                assert getattr(medium, p) == 'structural'

    def test_ok_loading_elastic(self, yaml_fn):
        params = ['E', 'nu', 'rho', 'eta']

        with open(yaml_fn, 'w') as fh:
            fh.write('medium_type: elastic\n')
            for ii, p in enumerate(params):
                fh.write('{}: {}\n'.format(p, ii))

        medium = from_yaml(yaml_fn)
        for ii, p in enumerate(params):
            assert getattr(medium, p) == ii

    def test_failed_forced_loading(self, yaml_fn):
        pem_params = ['phi', 'sigma', 'alpha', 'Lambda_prime', 'Lambda', 'rho_1', 'nu', 'E',
                  'eta', 'loss_type']
        eqf_params = ['phi', 'sigma', 'alpha', 'Lambda_prime', 'Lambda',
                  'rho_1', 'nu', 'E', 'eta']

        with open(yaml_fn, 'w') as fh:
            fh.write('medium_type: pem\n')
            for ii, p in enumerate(pem_params):
                if p!='loss_type':
                    fh.write('{}: {}\n'.format(p, ii))
                else:
                    fh.write('{}: structural\n'.format(p))

        medium = from_yaml(yaml_fn, EqFluidJCA)
        for ii, p in enumerate(eqf_params):
            assert getattr(medium, p) == ii


class TestMediaInstance:

    def test_instanciation_fluid(self):
        params = ['rho', 'c']
        medium = Fluid(**dict(zip(params, range(len(params)))))
        for ii, p in enumerate(params):
            assert getattr(medium, p) == ii

    def test_instanciation_eqf(self):
        params = ['phi', 'sigma', 'alpha', 'Lambda_prime', 'Lambda']
        medium = EqFluidJCA(**dict(zip(params, range(len(params)))))
        for ii, p in enumerate(params):
            assert getattr(medium, p) == ii

    def test_instanciation_elastic(self):
        params = ['E', 'nu', 'rho', 'eta']
        medium = Elastic(**dict(zip(params, range(len(params)))))
        for ii, p in enumerate(params):
            assert getattr(medium, p) == ii

    def test_instanciation_pem(self):
        params = ['phi', 'sigma', 'alpha', 'Lambda_prime', 'Lambda', 'rho_1', 'nu', 'E', 'eta']
        medium = PEM(**dict(zip(params, range(len(params)))), loss_type='structural')
        for ii, p in enumerate(params):
            assert getattr(medium, p) == ii
        assert medium.loss_type == 'structural'
