from Bio import Restriction
from Bio import SeqIO
import optparse
import sys

# Get all 
enzymes = Restriction.Restriction_Dictionary.rest_dict.keys()

def get_options():
    """
    This function allows commandline arguments to be passed to the script, so
    that you dont need to edit it every time you want to use a different 
    """
    parser = optparse.OptionParser('usage: %prog [options] ')
    parser.add_option(
        '-s',
        '--seqfile',
        dest='seqfile',
        help='File containing sequence to be analysed, as FASTA',
        metavar='FILE',
        default='')
    parser.add_option(
        '-e',
        '--enzyme',
        dest='enzyme',
        help='Enzyme',
        default="EcoRI")
    parser.add_option('-l',
        '--list-enzymes',
        dest='listenzymes',
        help='print list of enzymes',
        action="store_true",
        default=False)
    parser.add_option(
        '-m',
        "--min-length",
        dest="minlen",
        help="minimum length between restriction sites",
        default=200
        )
    parser.add_option(
        '-x',
        "--max-length",
        dest="maxlen",
        help="maximum length between restriction sites",
        default=600
        )
    options, args = parser.parse_args()
    die = False
    if options.enzyme not in Restriction.Restriction_Dictionary.rest_dict.keys():
        print "ERROR: %s is an invalid enzyme name" % options.enzyme
        die = True
    if not options.seqfile and not options.listenzymes:
        print "ERROR: seqfile is required"
        die = True
    
    # If there's something wrong with the options
    if die:
        parser.print_help()
        sys.exit(1)
    return options


# Store Commandline args
opts = get_options()

# If we've been asked to list all enzymes, do this now and exit
if opts.listenzymes:
    print "The following enzymes are supported"
    for enzyme in enzymes:
        print enzyme
    sys.exit(0)

# gets enzyme class by name
cutter = getattr(Restriction, opts.enzyme)  

# Opens file, and creates fasta reader
seq_file = open(opts.seqfile, "rb")
seqs = SeqIO.parse(seq_file, "fasta")

# Digest all sequences in the fasta file
count = 0
for record in seqs:
    record_count = 0

    # Do virtual digest
    fragments = cutter.catalyse(record.seq)
    
    # Find fragment lenghts
    fragment_lengths = []
    for seq in fragments:
        fragment_lengths.append(len(seq))

    # Count how many 
    for length in fragment_lengths:
        if length > opts.minlen and  length < opts.maxlen:
            record_count += 1
    
    # Append the counts for this record to the total sum
    count += record_count

    # Print summary
    """Comment this out by adding a pound at the start of the line if it
    annoys you"""
    print "%s has %i RADseq tags" % (record.id, record_count)

print "In total, %i RADseq tags were found" % count
