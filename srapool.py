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
    parser = ArgumentParser(description=desc)
    parser.add_argument(
        '-d', '--dumpcmd', required=False, default='fastq-dump --stdout {}',
        help='Shell pipeline to run on input SRA files')
    parser.add_argument(
        '-o', '--out', required=False, type=FileType('wb'), default=stdout,
        help='File path format string for output file. use {} to mark sample id.')
    parser.add_argument(
        '-j', '--jobs', required=False, default=1, type=int,
        help='Number of parallel dumping jobs')
    parser.add_argument('input_files', help='SRA Read files', type=str,
                        nargs="+")
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


def main():
    args = argparser().parse_args()

    for run in args.input_files:
        dump_sra(run, args.dumpcmd, args.out)
        print("Processed", run, file=stderr)


if __name__ == '__main__':
    main()
