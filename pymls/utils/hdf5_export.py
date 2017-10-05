#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# hdf5_export.py
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

from pymls import __VERSION__
import itertools
import numpy as np

try:
    import h5py
except ImportError:
    raise ImportError('Unable to load module h5py : please install it to use hdf5_export')

def __dump_in_group(group, r):

    datasets_shape = (len(r['f']), len(r['angle']), len(r['R'][0]))

    group.create_dataset('f', r['f'].shape, data=r['f'])
    group.create_dataset('angle', r['angle'].shape, data=r['angle'])
    dset = group.create_dataset('R', datasets_shape, dtype=np.dtype('complex'))
    for i_f, f in enumerate(r['f']):
        for i_a, a in enumerate(r['angle']):
            data_to_store = r['R'][i_f*len(r['angle'])+i_a]
            if r['enable_stochastic']:
                dset[i_f, i_a, :] = np.array(data_to_store)
            else:
                dset[i_f, i_a, :] = data_to_store



def hdf5_export(filename, resultset):
    """
    Traverse the resultset and outputs in to a HDF5 file
    """

    try:
        F = h5py.File(filename, 'w')
    except OSError as e:
        print(f'Unable to save into {filename} :\n\t{e}')
        return False

    if type(resultset)!=list:
        resultset = [resultset]

    seen_names = []
    for n, a in ((_['name'], _) for _ in resultset):
        if not n in seen_names:
            seen_names.append(n)
        elif not a['enable_stochastic']:
            raise ValueError('Two analysis with the same name present in the resultset')

    filtered = []
    for r in resultset:

        if r in filtered:
            continue

        G = F.create_group(r['name'])
        G.attrs['enable_stochastic'] = r['enable_stochastic']
        if r['enable_stochastic']:
            for a in filter(lambda _: _['name']==r['name'], resultset):
                filtered.append(a)

                subG = G.create_group('l'+str(a['stochastics']['layer'])+'_'+a['stochastics']['param'])
                __dump_in_group(subG, a)
        else:
            __dump_in_group(subG, a)

    F.close()

