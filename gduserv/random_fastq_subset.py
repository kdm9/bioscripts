#!/usr/bin/python
import HTSeq
import sys
import random

fraction = float(sys.argv[1])
in1 = iter(HTSeq.FastqReader(sys.argv[2]))
in2 = iter(HTSeq.FastqReader(sys.argv[3]))
out1 = open(sys.argv[4], "w")
out2 = open(sys.argv[5], "w")

while True:
    read1 = next(in1)
    read2 = next(in2)
    if random.random() < fraction:
        read1.write_to_fastq_file(out1)
        read2.write_to_fastq_file(out2)
out1.close()
out2.close()
