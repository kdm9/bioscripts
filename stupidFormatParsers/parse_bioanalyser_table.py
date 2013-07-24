from __future__ import print_function
import sys
from docopt import docopt

__doc__ = """
USAGE: parse_bioanalyser_table.py <file> ...
"""

def main():
    opts = docopt(__doc__)
    samples = {}
    for filename in opts["<file>"]:
        with open(filename) as fh:
            for line in fh:
                if line.startswith("Sample Name"):
                    sample_name = line.split(",")[1].strip()
                    samples[sample_name] = {}
                elif line.startswith("RNA Concentration"):
                    conc = line.split(",")[1].strip()
                    samples[sample_name]["conc"] = conc
                elif line.startswith("RNA Integrity Number"):
                    rin = line.split(",")[1].split()[0].strip()
                    samples[sample_name]["rin"] = rin

    print("Sample,Concentration,RIN")
    for sample, info in samples.iteritems():
        lne = "{samp},{conc},{rin}".format(
                samp=sample, conc=info["conc"], rin=info["rin"])
        print(lne)

if __name__ == "__main__":
    main()
