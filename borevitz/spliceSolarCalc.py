import argparse
import sys
from itertools import izip

def get_options():
    """
    This function allows commandline arguments to be passed to the script, so
    that you dont need to edit it every time you want to use a different 
    """
    parser = argparse.ArgumentParser('usage: %prog [options] ')
    parser.add_argument(
            '-o',
            '--outfile',
            dest='outfile',
            help='Output file',
            required=True
            )
    parser.add_argument(
            '-f',
            '--firstfile',
            dest='firstfile',
            help='First file',
            required=True
            )
    parser.add_argument(
            '-F',
            '--secondfile',
            dest='secondfile',
            help='Second file',
            required=True
            )
    parser.add_argument(
            '-1',
            '--numfirst',
            dest='numfirst',
            help='number of lines from first file',
            type=int,
            required=True
            )
    parser.add_argument(
            '-2',
            "--numsecond",
            dest="numsecond",
            help="number of lines from second file",
            type=int,
            required=True
            )
    parser.add_argument(
            '-H',
            "--headerlen",
            dest="headerlen",
            help="Indicate a header of HEADERLEN lines exists, and should be "
                "skipped. Use --headerlen=0 to indicate no header. DEFAULT=1",
            type=int,
            default=1)
    parser.add_argument(
            '-v',
            "--verbose",
            dest="verbose",
            action="count"
            )
    options = parser.parse_args()
    return options


def main():
    # Store Commandline args
    opts = get_options()

    fh1 = open(opts.firstfile)
    fh2 = open(opts.secondfile)
    ofh = open(opts.outfile, "w")

    for iii in xrange(opts.headerlen):
        _ = next(fh1)
        _ = next(fh2)

    f1lines = 0
    f2lines = 0
    source = 1
    for f1line, f2line in izip(fh1, fh2):
        if f1lines == opts.numfirst:
            f1lines = 0
            source = 2
        if f2lines == opts.numsecond:
            f2lines = 0
            source = 1

        if source == 1:
            ofh.write(f1line)
            f1lines += 1
        elif source == 2:
            ofh.write(f2line)
            f2lines += 1

if __name__ == "__main__":
    main()
