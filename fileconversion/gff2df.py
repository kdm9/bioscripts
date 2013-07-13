from __future__ import print_function
from docopt import docopt
import json

__doc__ = """
USAGE:
    gff2df [-c FEATURE_CLASSES] <gff_in> <dataframe>

OPTIONS:
    -c FEATURE_CLASSES	Comma-seperated list of features to extract
"""


def _get_note_dict(note_str):
    notes = note_str.split(";")
    note_dict = {}
    for note in notes:
        key, value = note.split("=")
        note_dict[key] = value
    return note_dict


def _make_record(fields):
    chr = fields[0]
    start = fields[3]
    end = fields[4]
    strand = fields[6]
    notes = _get_note_dict(fields[8])
    tabline = "%s\t%s\t%s\t%s\t%s\t%s\n" % \
    	(notes["ID"], chr, start, end, strand, json.dumps(notes))
    return tabline


def main():
    opts = docopt(__doc__)
#    opts  = {
#    	"<gff_in>": "/home/pete/workspace/refseqs/TAIR10_gen/TAIR10_GFF3_genes_transposons.gff",
#    	"<dataframe>": "/home/pete/workspace/refseqs/TAIR10_gen/TAIR10_GFF3_genes_transposons.annot.tab",
#    	"-c": True,
#    	"FEATURE_CLASSES": "chromosome"
#    	}

    if opts["-c"]:
    	classes = opts["-c"].split(",")
    else:
    	classes = ["gene",]

    gff_fh = open(opts["<gff_in>"])
    tab_fh = open(opts["<dataframe>"], "w")
    tab_fh.write("GeneID\tChr\tStart\tEnd\tStrand\tNotes\n")
    for line in gff_fh:
    	fields = line.split()
    	if fields[2] in classes:
    		tabline = _make_record(fields)
    		tab_fh.write(tabline)
    gff_fh.close()
    tab_fh.close()

if __name__ == "__main__":
    main()
