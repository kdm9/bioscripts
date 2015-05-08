####################
# p-distance calculator
# lteasnail 20150505
##
# This script will calculate the pairwise-distance (p-distance) between two
# specified sequences. P-distance is calculated by counting the number of bases
# that differ between the two sequences and dividing the number of differences
# by the length of the alignment minus any base pairs which are missing in either
# sequence. The sequences need to be aligned and the alignments need to be of the
# same length.
##
# Run as follows: python p-distance_script.py file.fasta header_seq1 header_seq2 > output.txt
# e.g. python p-distance_script.py 52083_aa_23_[2]_sc_trim.fas 02~~comp11592_c0_seq1~~1E-162~~1 25~~comp75444_c0_seq1~~1E-159~~1
####################

#the fasta parser
import screed
#for taking arguments from the command line
import sys


file = sys.argv[1]
seq_1_name = sys.argv[2]
seq_2_name = sys.argv[3]

# Find the two selected sequences and 
# convert them to seperated lists 
for seq in screed.open(file):
    if seq.name == seq_1_name:
        seq_1 = seq.sequence
        seq_1_split = list(seq_1)
        length = len(seq.sequence)
    elif seq.name == seq_2_name:
        seq_2 = seq.sequence
        seq_2_split = list(seq_2)
    else:
        continue

        
# Count the number of bases with missing data and 
# the number where the two sequences differ
num_missing = 0
num_diff = 0

for base in range(len(seq_1_split)):
    if seq_1_split[base] == '-' or seq_2_split[base] == '-':
        num_missing = num_missing + 1
        continue 
    elif seq_1_split[base] != seq_2_split[base]:
        num_diff = num_diff + 1
    else:
        continue

# Calulate and print the p-distance
num_diff = float(num_diff)

if num_diff == 0:
    print 'no differences'
else:
    pdistance = num_diff / (length - num_missing)
    part = length - num_missing
    pd = num_diff / part
    print '%s\t%r\t%d\t%d' % (file, pd, num_diff, part)
    
