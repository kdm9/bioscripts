from __future__ import print_function
from gffutils import FeatureDB, create_db
from docopt import docopt
import os


__doc__ = """
USAGE: make_intergenes.py [-o OUTFILE] <infile>

OPTIONS:
    -o OUTFILE      Output file. By default, stdout.
"""


def _print_intergene(chrom, start, stop, name):
    print("{chrom}\tTAIR10\tintergene\t{stt}\t{stp}\t.\t.\t.\tID={nm}".format(
                chrom=chrom, stt=start, stp=stop, nm=name))


def main():
    opts = docopt(__doc__)
    gff_fn = opts["<infile>"]
    db_fn = gff_fn + ".db"

    if not os.path.exists(db_fn):
        create_db(gff_fn, db_fn)

    fdb = FeatureDB(db_fn)

    assert "gene" in list(fdb.featuretypes()), "Database doesn't contain genes"
    for chrom in fdb.chromosomes():
        last_stop = 0
        last_id = chrom + "_START"
        genes = list(fdb.features_of_type("gene", chrom=chrom))
        genes.extend(list(fdb.features_of_type("transposable_element",
                chrom=chrom)))
        genes.extend(list(fdb.features_of_type("transposable_element_gene",
                chrom=chrom)))
        genes = sorted(genes, key=lambda g: g.start)
        print(fdb[chrom])

        for gene in genes:
            start = gene.start
            stop = gene.stop
            agi = gene.id

            if start > last_stop:
                ig_name = last_id + "-" + agi
                ig_start = last_stop + 1  # starts at the next pos
                ig_stop = start - 1  # stops before the next gene
                _print_intergene(chrom, ig_start, ig_stop, ig_name)
            print(gene)
            for transcript in fdb.children(gene):
                print(transcript)
                for exon in fdb.children(transcript):
                    print(exon)
            last_stop = stop
            last_id = agi


if __name__ == "__main__":
    main()
