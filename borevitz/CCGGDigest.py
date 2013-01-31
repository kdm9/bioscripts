from Bio import Restriction
from Bio import SeqIO


cutter = Restriction.MspI
transcripts_file = open("BdGDB_192_cdna.fasta", "rb")
transcripts = SeqIO.parse(transcripts_file, "fasta")

count = 0
for transcript in transcripts:
    fragments = cutter.catalyse(transcript.seq)
    fragment_lengths = []
    for seq in fragments:
        fragment_lengths.append(len(seq))

    for length in fragment_lengths:
        if length > 200 and  length < 600:
            count += 1
print count
