import re
from sys import argv
fh = open(argv[1])
this_peak = []
for line in fh:
    if line != "-----\n":
        this_peak.append(line)
    else:
        this_peak = "".join(this_peak)
        csv_peak = this_peak.replace('\t\n', '\t"\n')
        csv_peak += "\""
        print csv_peak
        this_peak = []

