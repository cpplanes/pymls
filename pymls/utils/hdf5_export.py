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

from pymls.layers import StochasticLayer
import pymls.backing as backing
import numpy as np

try:
    import h5py
except ImportError:
    raise ImportError('Unable to load module h5py : please install it to use hdf5_export')


def __dump_in_group(group, r, output_T=False):

    datasets_shape = (len(r['f']), len(r['angle']), len(r['R'][0]))

    group.create_dataset('f', r['f'].shape, data=r['f'])
    group.create_dataset('angle', r['angle'].shape, data=r['angle'])

    coeffs = ['R', 'T'] if output_T else ['R']
    for name in coeffs:
        dset = group.create_dataset(name, datasets_shape, dtype=np.dtype('complex'))
        for i_f, f in enumerate(r['f']):
            for i_a, a in enumerate(r['angle']):
                data_to_store = r[name][i_f*len(r['angle'])+i_a]
                if r['enable_stochastic']:
                    dset[i_f, i_a, :] = np.array(data_to_store)
                else:
                    dset[i_f, i_a, :] = data_to_store

    if r['enable_stochastic']:
        draws = r['stochastics']['values']
        group.create_dataset('stochastic_values', (len(draws),), dtype=type(draws[0]), data=draws)
        group.attrs['param'] = r['stochastics']['param']
        group.attrs['layer'] = r['stochastics']['layer']


def hdf5_export(filename, S):
    """
    Traverse the Solver S's resultset and outputs in to a HDF5 file
    """

    try:
        F = h5py.File(filename, 'w')
    except OSError as e:
        print('Unable to save into {} :\n\t{}'.format(filename, str(e)))
        return False

    # normalise the type of resultset
    resultset = [S.resultset] if type(S.resultset) != list else S.resultset

    # check that no two analyses share the name
    # except if it includes stochastic analysis
    seen_names = []
    for n, a in ((_['name'], _) for _ in resultset):
        if n not in seen_names:
            seen_names.append(n)
        elif not a['enable_stochastic']:
            raise ValueError('Two analysis with the same name present in the resultset')

    dt_str = h5py.special_dtype(vlen=str)
    metadata_group = F.create_group('meta')

    # save the definition of the multilayer
    layers_group = metadata_group.create_group('layers')
    layers_group.attrs['transmission'] = S.backing == backing.transmission
    layers_group.create_dataset('media', data=np.array([_.medium for _ in S.layers], dtype=object), dtype=dt_str)
    layers_group.create_dataset('thickness', data=np.array([_.thickness for _ in S.layers]))
    layers_group.create_dataset('stochastic', data=np.array([type(_) == StochasticLayer for _ in S.layers]))

    # save PRNG state
    prng_dset = metadata_group.create_dataset('prng_state', S.prng_state[1].shape, data=S.prng_state[1])
    prng_dset.attrs['prng'] = S.prng_state[0]
    prng_dset.attrs['pos'] = S.prng_state[2]
    prng_dset.attrs['has_gauss'] = S.prng_state[3]
    prng_dset.attrs['cached_gaussian'] = S.prng_state[4]

    # dump all analyses, one per group
    filtered = []
    for r in resultset:

        if r in filtered:  # stochastic analyses are filtered out
            continue

        G = F.create_group(r['name'])
        G.attrs['enable_stochastic'] = r['enable_stochastic']
        if r['enable_stochastic'] and len(resultset) > 1:
            # if r is stochastic, output every variant in a row and filter them for later
            for a in filter(lambda _: _['name'] == r['name'], S.resultset):
                filtered.append(a)

                subG = G.create_group(str(a['stochastics']['layer'])+'_'+a['stochastics']['param'])
                __dump_in_group(subG, a, S.backing == backing.transmission)
        else:
            __dump_in_group(G, r, S.backing == backing.transmission)

    F.close()
