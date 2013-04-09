#!/usr/bin/env python
from Bio.Blast import NCBIXML
from Bio.SeqIO.FastaIO import FastaWriter
from Bio.Entrez import efetch
from Bio import Entrez
import re
Entrez.email = "abc@gmail.com"
import sys
EXPECT = 0.001

processed_ids = {}
input_filehandle = open(sys.argv[1])
output_filehandle = open(sys.argv[2], "w")
blast_parser = NCBIXML.parse(input_filehandle)
for record in blast_parser:
    print "%s (within db %s found %i hits)" % (record.query, record.database, 250)
    for aln in record.alignments:
        print "\t%s" % aln.hit_id
        hit_gi = int(aln.hit_id.split("|")[1])
        if hit_gi in processed_ids:
            continue
        else:
            processed_ids[hit_gi] = None
    if "LOW QUALITY" in aln.hit_def:
            continue
        for hsp in aln.hsps:
            if float(hsp.expect) < EXPECT:
                qlen = len(hsp.query.replace("-",""))
                coverage = (float(qlen)/ float(record.query_letters))*100.0
                if coverage > 80.0:
                    print "\t\tExp: %f start: %i Qend: %i Coverage%%: %f" % (float(hsp.expect), hsp.query_start, hsp.query_end, coverage)
                    ef_handle = efetch(db="protein", id=hit_gi, rettype="fasta", retmode="text")
                    fasta_txt = ef_handle.read()
                    # edit fasta_txt

                    fasta_txt = fasta_txt.replace('predicted protein', 'pred.')
                    fasta_txt = fasta_txt.replace('hypothetical protein', 'pred.')
                    fasta_txt = fasta_txt.replace('PREDICTED:', 'pred.')
                    fasta_txt = fasta_txt.replace('probable', '')
                    fasta_txt = re.sub("glycerol.*?phosphate.*?acyltransferase", "GPAT", fasta_txt, re.I)
                    fasta_txt = re.sub("\[(\S)\S+", "[\\1", fasta_txt)
                    fasta_txt = re.sub("\[(\w) (\S{3}).+?\]", "[\\1 \\2]", fasta_txt)
                    fasta_txt = re.sub(">gi\|(\d+)\|\S+ (.+?)\[(.+?)\]", ">\\2|[\\3]|\\1", fasta_txt)
                    fasta_txt = re.sub("\s+", " ", fasta_txt)
                    fasta_txt = fasta_txt.replace(' ','_')
                    #print fasta_txt
                    output_filehandle.write(fasta_txt)
                    output_filehandle.flush()
input_filehandle.close()
output_filehandle.close()
