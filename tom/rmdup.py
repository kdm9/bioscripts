from Bio import pairwise2
from Bio.SeqIO import FastaIO
from sys import argv

pairwise2.MAX_ALIGNMENTS = 100
MAX_SCORE = 0.95
MIN_SCORE = 0.20
input_filehandle = open(argv[1])
output_filehandle = open(argv[2], "w")

fasta_lst = list(FastaIO.SimpleFastaParser(input_filehandle))
#non_dups = []

while len(fasta_lst) >= 2:
    needle_rec = fasta_lst.pop()
    print needle_rec[0].split()[0]
    keep = False
    for haystack_rec in fasta_lst:
        print "\t%s" % haystack_rec[0].split()[0]
        alns = pairwise2.align.globalxx(needle_rec[1], haystack_rec[1])
        print "\t\tgot %i alns" % len(alns)
        sort_alns = []
        for aln in alns:
            score = float(aln[2]) / float(aln[4])
            # pack score and aln in tuple, so we can sort by score
            sort_alns.append((score, aln))
        sort_alns = list(reversed(sorted(sort_alns)))  # sort desc
        best_aln = sort_alns.pop()
        print "\t\tSorted, best aln score is %f" %  best_aln[0]
        if best_aln[0] > MAX_SCORE or best_aln[0] < MIN_SCORE:  # aln[0] is score, see above
            if haystack_rec[0].find("pred") >= 0:
                needle_rec = haystack_rec
            break
        else:
            keep = True
    if keep:
        print "Writing seq: %s" % needle_rec[0]
        output_filehandle.write("%s\n%s\n" % needle_rec)
        output_filehandle.flush()
input_filehandle.close()
output_filehandle.close()

