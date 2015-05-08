# Copyright 2015 Luisa Teasdale
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
# Run as follows:
# python p-distance_script.py name1 name2 file.fa file2.fa > output.txt
####################

# the fasta parser
import screed

def process_file(file, seq_1_name, seq_2_name):
    """Calculates the P distance between the two sequences in a file"""
    # Find the two selected sequences and convert them to seperated lists
    seq_1 = None
    seq_2 = None
    for seq in screed.open(file):
        if seq.name == seq_1_name:
            seq_1 = seq.sequence
        elif seq.name == seq_2_name:
            seq_2 = seq.sequence
        if seq_1 is not None and seq_2 is not None:
            break

    if seq_1 is None:
        print "ERROR: Couldn't find seq 1, check your spelling"
        exit(1)
    if seq_2 is None:
        print "ERROR: Couldn't find seq 2, check your spelling"
        exit(1)

    length = len(seq_1)
    if len(seq2) != length:
        print "ERROR: The two sequence lengths differ"
        exit(1)

    # Count the number of bases with missing data and the number where the two
    # sequences differ
    num_missing = 0
    num_diff = 0
    for base in range(length):
        if seq_1[base] == '-' or seq_2[base] == '-':
            num_missing += 1
        elif seq_1[base] != seq[base]:
            num_diff += 1

    # Calulate and print the p-distance
    num_diff = float(num_diff)
    if num_diff == 0:
        print '%s\t0\t0\t0' % file
    else:
        part = length - num_missing
        pdistance = num_diff / part
        print '%s\t%r\t%d\t%d' % (file, pdistance, num_diff, part)

if __name__ == "__main__":
    # for taking arguments from the command line
    import sys

    seq_1_name = sys.argv[1]
    seq_2_name = sys.argv[2]

    for file in sys.argv[3:]:
        process_file(file, seq_1_name, seq_2_name)
