#!/usr/bin/env python3
# Copyright 2016 Kevin Murray <spam@kdmurray.id.au>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, division, absolute_import

from mpi4py import MPI

import itertools as itl
from glob import glob
import gzip
import os
from os import path, mkdir
import re
from sys import stderr, stdout
from subprocess import DEVNULL, PIPE, Popen
import json
from argparse import (
    ArgumentParser,
    FileType,
)
from textwrap import dedent
CHUNK = 2**24


def mpisplit(things, comm):
    '''Split `things` into a chunk for each MPI rank.'''
    pieces = None
    rank = comm.Get_rank()
    if rank == 0:
        size = comm.Get_size()
        if size > len(things):
            print('Number of MPI ranks is greater than number of items')
            print('This is harmless but silly')
        pieces = [list() for x in range(size)]
        for i, thing in enumerate(things):
            pieces[i % size].append(thing)
    return comm.scatter(pieces, root=0)


def argparser():
    desc = "Pools SRA runs into a single fastq per sample"
    el = "Sample map is a JSON file mapping sample name to list of SRA files"
    parser = ArgumentParser(description=desc, epilog=el)
    parser.add_argument(
        '-d', '--precmd', required=False, default='fastq-dump --stdout {}',
        help='Shell pipeline to run on input SRA files')
    # parser.add_argument(
    #     '-c', '--postcmd', required=False,
    #     help='Shell pipeline to run on output files before saving to disk')
    parser.add_argument(
        '-i', '--infile', required=False, default='./{}.sra',
        help='File path format string for input file. use {} to mark SRA id.')
    parser.add_argument(
        '-o', '--outfile', required=False, default='./{}.fastq.gz',
        help='File path format string for output file. use {} to mark sample id.')
    parser.add_argument('samplemap', help='Read files', type=FileType('r'))
    return parser


def dump_sra(srafile, dumpcmd, outstream):
    dump_cmd = dumpcmd.format(' "{}"'.format(srafile))
    with Popen(dump_cmd, shell=True, executable='/bin/bash', stdin=DEVNULL,
               stdout=PIPE, stderr=None, universal_newlines=False) as proc:
        while True:
            buf = proc.read(CHUNK)
            if not buf:
                break
            outstream.write(buf)


def process_sample(samplefile, srafiles, dumpcmd, postcmd=None):
    out_fh = gzip.open(samplefile, 'wb', compresslevel=9)
    try:
        for srafile in srafiles:
            dump_sra(srafile, dumpcmd, out_fh)
    finally:
        out_fh.close()


def main():
    args = argparser().parse_args()
    print(args)

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    samples = json.load(args.samplemap)
    sample_map = mpisplit(samples.items(), comm)
    print(rank, sample_map)

    for sample, runs in sample_map:
        samplefile = args.outfile.format(sample)
        runfiles = [args.infile.format(run) for run in runs]
        process_sample(samplefile, runfiles, args.dumpcmd)


if __name__ == '__main__':
    main()
