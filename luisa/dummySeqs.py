#!/usr/bin/env python
import Bio
from Bio.SeqIO import index as index_seqfile
from Bio.SeqIO import write as write_seqfile
from Bio.Seq import Seq
from Bio.SeqRecord import  SeqRecord
from os import path
from docopt import docopt


CLI = """
USAGE:
    d.py <species_list> <out_dir> <gene_alignment> [<gene_alignment> ...]

"""

def split_id_line(line):
    return line.strip().split('~~')[0]

def process_gene_file(fle, list_of_sp, out_dir):
    with open(fle) as fh:
        idx = index_seqfile(fle, "fasta", key_function=split_id_line)
    seqs = []
    for id, seq in idx.iteritems():
        seqs.append(seq)
    len_of_seq = len(seqs[0].seq)
    dummy = '~' * len_of_seq
    for sp in list_of_sp:
        if sp not in idx:
            name = sp + "~~dummy"
            dummy_s = Seq(dummy)
            dummy_sr = SeqRecord(dummy_s, id=name, name=name, description='KDM FUCKED THIS UP')
            seqs.append(dummy_sr)
    outfile = path.join(out_dir, path.basename(path.splitext(fle)[0] + "_fixed.fas"))
    seqs = sorted(seqs, key=lambda s: s.id)
    with open(outfile, "w") as ofh:
        write_seqfile(seqs, ofh, "fasta")
    return seqs

if __name__ == "__main__":
    opts = docopt(CLI)
    alignments = opts['<gene_alignment>']
    species_file = opts['<species_list>']
    out_dir = opts['<out_dir>']
    with open(species_file) as fh:
        list_of_sp = [s.strip() for s in fh.readlines()]
    for gene_file in alignments:
        print "Procesing", gene_file,
        process_gene_file(gene_file, list_of_sp, out_dir)
        print "done"
