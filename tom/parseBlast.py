#!/usr/bin/env python
from Bio.Blast import NCBIXML
from Bio.SeqIO.FastaIO import FastaWriter
from Bio.Entrez import efetch
from Bio import Entrez
import re
from time import sleep
Entrez.email = "u4841401@anu.edu.au"
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
            print '\t\t"LOW QUALITY" in seq name'
            continue
        for hsp in aln.hsps:
            if float(hsp.expect) < EXPECT:
                qlen = len(hsp.query.replace("-",""))
                coverage = (float(qlen)/ float(record.query_letters))*100.0
                if coverage > 80.0:
                    sleep(5)
                    print "\t\tExp: %f start: %i Qend: %i Coverage%%: %f" % (float(hsp.expect), hsp.query_start, hsp.query_end, coverage)
                    ef_handle = efetch(db="protein", id=hit_gi, rettype="fasta", retmode="text")
                    fasta_txt = ef_handle.read()
                    while fasta_txt.find("unavailable") >=0:
                        print "\t\tentrez is failing hard. sleeping. (id:%i)" % hit_gi
                        sleep(5)
                        ef_handle = efetch(db="protein", id=hit_gi, rettype="fasta", retmode="text")
                        fasta_txt = ef_handle.read()

                    # edit fasta_txt
                    fasta_lines = fasta_txt.splitlines()
                    fasta_header = fasta_lines[0]
                    fasta_seq = "".join(fasta_lines[1:])

                    fasta_header = fasta_header.replace('predicted protein', 'pred.')
                    fasta_header = fasta_header.replace('hypothetical protein', 'pred.')
                    fasta_header = fasta_header.replace('PREDICTED:', 'pred.')
                    fasta_header = fasta_header.replace('probable', '')
                    fasta_header = re.sub("glycerol.*?phosphate.*?acyltransferase", "GPAT", fasta_header, re.I)
                    fasta_header = re.sub("\[(\S)\S+", "[\\1", fasta_header)
                    fasta_header = re.sub("\[(\w) (\S{3}).+?\]", "[\\1 \\2]", fasta_header)
                    fasta_header = re.sub(">gi\|(\d+)\|\S+ (.+?)\[(.+?)\]", ">\\2|[\\3]|\\1", fasta_header)
                    fasta_header = re.sub("\s+", " ", fasta_header)
                    fasta_header = fasta_header.replace(' ','_')
                    fasta_txt = "%s\n%s\n\n" % (fasta_header, fasta_seq)
                    #print fasta_txt
                    output_filehandle.write(fasta_txt)
                    output_filehandle.flush()
                else:
                    print "\t\tPoor coverage"
            else:
                print "\t\tExpect value too high"
input_filehandle.close()
output_filehandle.close()
