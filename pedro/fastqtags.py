#!/usr/bin/env python
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

from __future__ import print_function, division
from collections import Counter
from sys import argv, stderr, stdout

import screed

if len(argv) != 2:
    print("USAGE: fastqtags.py <fastq>", file=stderr)
    exit(1)

fqpath = argv[1]

tags = Counter()
print("Counting reads", file=stderr)
with screed.open(fqpath) as fqfile:
    for i, read in enumerate(fqfile):
        tags[read.sequence] += 1
        if i % 10000 == 0:
            print("   ...", i, "reads", file=stderr)
    print("Finished, counted", i + 1, "reads", file=stderr)

# Python2 vs python3 compat hack
try:
    tag_iter = tags.iteritems()
except:
    tag_iter = tags.items()

for tag, count in tag_iter:
    print(tag, count, sep='\t')

print("All done!", file=stderr)
