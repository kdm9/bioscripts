#!/usr/bin/env python
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
