import re
import sys
from datetime import datetime

infile = sys.argv[1]
outfile = sys.argv[2]

in_fh = open(infile)
out_fh = open(outfile, "w")
out_fh.write("'ISO Date','Temperature','Humidity'\n")

at_start = False
for line in in_fh:
    while not line.startswith("-") and not at_start:
        line = next(in_fh)
    while not line.find("%RH") > 0:
        line = next(in_fh)
    at_start = True
    fields = line.strip().split()
    date = datetime.strptime(fields[5], "%d-%m-%y/%H:%M:%S")
    temp = float(fields[1])
    rh = float(fields[3])
    csv_line = "'%s',%f,%f\n" % (date.isoformat(), temp, rh)
    out_fh.write(csv_line)

in_fh.close()
out_fh.close()
