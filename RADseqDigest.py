#!/usr/bin/env python
from Bio import Restriction
from Bio import SeqIO
import optparse
import sys

# Get all enzymes supported by the Bio.Retriction module
enzymes = Restriction.Restriction_Dictionary.rest_dict.keys()

def get_options():
    """
    This function allows commandline arguments to be passed to the script, so
    that you dont need to edit it every time you want to use a different set of
    settings.
    """
    parser = optparse.OptionParser('usage: %prog [options] ')
    parser.add_option(
            '-s',
            '--seqfile',
            dest='seqfile',
            help='File containing sequence to be analysed, as FASTA',
            metavar='FILE',
            default=''
            )
    parser.add_option(
            '-e',
            '--enzyme',
            dest='enzyme',
            help='Enzymes. Use a comma seperated list e.g. MspI,HpaII',
            default="EcoRI"
            )
    parser.add_option(
            '-l',
            '--list-enzymes',
            dest='listenzymes',
            help='print list of enzymes',
            action="store_true",
            default=False
            )
    parser.add_option(
            '-c',
            "--count",
            dest="count",
            help="count all restriction sites, equivalent to -m 0 -x infinity",
            action="store_true",
            default=False
            )
    parser.add_option(
            '-m',
            "--min-length",
            dest="minlen",
            help="minimum length between restriction sites",
            type=int,
            default=200
            )
    parser.add_option(
            '-x',
            "--max-length",
            dest="maxlen",
            help="maximum length between restriction sites",
            type=int,
            default=600
            )
    parser.add_option(
            '-v',
            "--verbose",
            dest="verbose",
            action="count"
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

def main(opts):
    """Does the actual digestions given an option namespace"""
    # If we've been asked to list all enzymes, do this now and exit
    if opts.listenzymes:
        print "The following enzymes are supported"
        for enzyme in enzymes:
            print enzyme
        sys.exit(0)

    # gets enzyme class by name
    cutters = opts.enzyme.split(",")
    cutters = [getattr(Restriction, enz) for enz in cutters]
    print("Using the following exzymes:")
    for cutter in cutters:
        print("\t{}".format(cutter))
        print("\t{}".format(cutter.site))

    # Opens file, and creates fasta reader
    seq_file = open(opts.seqfile, "rb")
    seqs = SeqIO.parse(seq_file, "fasta")

    # Digest all sequences in the fasta file
    count = 0
    for record in seqs:
        record_count = 0
        # When we're counting, we only want to show how many cut sites there
        # are. Given that cutting a sequence 0 times gives one fragment, we
        # need to decrement this, or we add one to the true number of sites

        # Do virtual digest
        # TODO: change this to use `cutters` and RestrictionBatch
        fragments = cutter.catalyse(record.seq)

        # Find fragment lenghts
        fragment_lengths = []
        for seq in fragments:
            fragment_lengths.append(len(seq))

        # Count how many fragments meet the specified selection criteria
        for length in fragment_lengths:
            if opts.count:  # Count everything
                record_count += max(0, len(fragment_lengths) - 1)
            elif length > opts.minlen and  length < opts.maxlen:
                record_count += 1

        # Append the counts for this record to the total sum
        count += record_count

        if opts.verbose > 0:
            # Print summary
            print "%s has %i RADseq tags" % (record.id, record_count)

    print "In total, %i RADseq tags were found" % count

if __name__ == "__main__":
    # Store Commandline args
    opts = get_options()
    main(opts)
