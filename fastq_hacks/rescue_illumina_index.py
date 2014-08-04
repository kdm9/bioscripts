from __future__ import print_function
from collections import Counter
import docopt
import itertools import (
    izip,
    cycle,
)
import re
import sys
import multiprocessing as mp
from skbio.core.alignment import StripedSmithWaterman

CLI = """

USAGE:
rescue_illumina_index.py -i IN_FQ -o OUT_FQ -a ADAPTOR

OPTIONS:
    -i IN_FQ    Input fastq
    -o OUT_FQ   Ouput fastq
    -a ADAPTOR  Adaptor sequence, with barcode as Ns

The index of the first N (from the left) in the adaptor sequence is assumed to
be the start site of the barcode. The first N from the right is assumed to be
the end, and end - start is assumed to be the length.

"""


def fq(fhandle):
    for h, s, _, q in izip(fhandle, fhandle, fhandle, fhandle):
        #yield (h.strip(), s.strip(), _.strip(), q.strip())
        yield (h, s, _, q)


def match_read((read, adapt, bcd_start, bcd_end)):
    aln = adapt(read[1])
    bcd = "NOBCD"
    if aln.target_begin > 10 and aln.target_begin < 30:
        seq = read[1][:aln.target_begin]
        bcd_start = aln.target_begin + 33
        bcd = read[1][bcd_start:bcd_start + 6]
        seq = "{}{}\n".format(bcd, seq)
        qual =  "{}{}\n".format(read[3][bcd_start:bcd_start + 6], read[3][:aln.target_begin])
        read = (read[0], seq, "+\n", qual)
    return (bcd, read)

if __name__ == "__main__":
    ifp = open(sys.argv[1])
    ctr = Counter()
    iii = 0
    adapt = opts['-a']
    adapt_matcher = StripedSmithWaterman(adapt)
    bcd_start = adapt.index("N")
    bcd_end = adapt.rindex("N")
    for bcd, read in pool.imap(match_read,
                              izip(fq(ifp),
                                   cycle(adapt_matcher),
                                   cycle(bcd_start),
                                   cycle(bcd_end))):
        if iii % 100 == 0:
            print("Processed {: 7d} reads. Seen {} barcodes".format(
                iii, len(ctr)), end = '\r', file=sys.stderr)
        iii += 1
        ctr[bcd] += 1
        print("{}{}{}{}".format(*read), end='')
    print("Processed {: 7d} reads. Seen {} barcodes".format(iii, len(ctr)),
          file=sys.stderr)
    for k, v in ctr.most_common():
        print("{}\t{: 6d}".format(k, v), file=sys.stderr)
