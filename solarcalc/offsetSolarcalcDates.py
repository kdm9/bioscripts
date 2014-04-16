from csv import DictReader, DictWriter
from docopt import docopt
import sys
from datetime import datetime, timedelta

__doc__ = """
USAGE:
    script.py [ -i INFILE -o OUTFILE ] -d DAYS

OPTIONS:
    -d DAYS     Integral number of days to offset file by. Negative for
                    backwards in time, positive for forwards in time.
    -i INFILE   Input solarcalc CSV file. [stdin]
    -o OUTFILE  Output solarcalc CSV file. [stdout]
"""


def main():
    opts = docopt(__doc__)

    try:
        if int(opts["-d"]) != 0:
            offset = int(opts["-d"])
        else:
            raise ValueError
    except ValueError:
        sys.stderr.write("ERROR: value for -d must be a non-zero number\n")

    if "-i" in opts and opts["-i"]:
        in_fh = open(opts["-i"])
    else:
        in_fh = sys.stdin
    if "-o" in opts and opts["-o"]:
        out_fh = open(opts["-o"], "w")
    else:
        out_fh = sys.stdout

    csv_keys = [
            "Date", "Time", "ChamTemp", "ChamRH", "LED1", "LED2", "LED3", 
            "LED4", "LED5", "LED6", "LED7", "Total Solar (Watt/m2)",
            "Simulated Date-Time "
            ]

    reader = DictReader(in_fh)
    writer = DictWriter(out_fh, csv_keys)
    writer.writeheader()

    for line in reader:
        date = datetime.strptime(line["Date"], "%m/%d/%Y")
        newdate = date + timedelta(offset)
        line["Date"] = newdate.strftime("%m/%d/%Y")
        writer.writerow(line)

    in_fh.close()
    out_fh.close()

if __name__ == "__main__":
    main()
