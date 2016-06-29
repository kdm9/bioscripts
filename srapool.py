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

from argparse import (
    ArgumentParser,
    FileType,
)
from glob import glob
import gzip
import itertools as itl
import json
import multiprocessing as mp
import os
from os import path, mkdir
import re
from sys import stderr, stdout
from subprocess import DEVNULL, PIPE, Popen
from textwrap import dedent

CHUNK = 2**26


def argparser():
    desc = "Pools SRA runs into a single fastq per sample"
    el = "Sample map is a JSON file mapping sample name to list of SRA files"
    parser = ArgumentParser(description=desc, epilog=el)
    parser.add_argument(
        '-d', '--dumpcmd', required=False, default='fastq-dump --stdout {}',
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
    parser.add_argument(
        '-j', '--jobs', required=False, default=1, type=int,
        help='Number of parallel dumping jobs')
    parser.add_argument('samplemap', help='Read files', type=FileType('r'))
    return parser


def dump_sra(srafile, dumpcmd, outstream):
    dump_cmd = dumpcmd.format(' "{}"'.format(srafile))
    with Popen(dump_cmd, shell=True, executable='/bin/bash', stdin=DEVNULL,
               stdout=PIPE, stderr=None, universal_newlines=False) as proc:
        while True:
            buf = proc.stdout.read(CHUNK)
            if not buf:
                break
            outstream.write(buf)


def process_sample(samplefile, srafiles, dumpcmd, postcmd=None, quiet=False):
    out_fh = gzip.open(samplefile, 'wb', compresslevel=6)
    try:
        for srafile in srafiles:
            dump_sra(srafile, dumpcmd, out_fh)
    finally:
        out_fh.close()
    if not quiet:
        print("Processed", samplefile, file=stderr)


def main():
    args = argparser().parse_args()

    sample_map = json.load(args.samplemap)

    arg_lists = []
    for sample, runs in sample_map.items():
        samplefile = args.outfile.format(sample)
        runfiles = [args.infile.format(run) for run in runs]
        arg_lists.append((samplefile, runfiles, args.dumpcmd))

    pool = mp.Pool(args.jobs)
    pool.starmap(process_sample, arg_lists)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
