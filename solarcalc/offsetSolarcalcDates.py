from csv import DictReader, DictWriter
from docopt import docopt
import sys
from datetime import datetime, timedelta

__doc__ = """
USAGE:
    script.py -d DAYS -i INFILE -o OUTFILE

OPTIONS:
    -d DAYS     Integral number of days to offset file by. Negative for
                    backwards in time, positive for forwards in time.
    -i INFILE   Input solarcalc CSV file
    -o OUTFILE  Output solarcalc CSV file
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

    in_fh = open(opts["-i"])
    out_fh = open(opts["-o"], "w")

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
