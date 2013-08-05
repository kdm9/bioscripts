from __future__ import print_function
from bs4 import BeautifulSoup
from docopt import docopt

__doc__ = """
USAGE:
   parse_bioanalyser_html_report.py [-e -g -d] <input_toc_file> <output_dir>

OPTIONS:
    -e          Extract electrophoretograms
    -g          Extract gels
    -d          Extract data tables (RIN, concentration, etc)

input_toc_file  A *_TOC.html file from the agilent software
output_dir      Dir to place images/tables in. Will be created if it does not
                    exist
"""


def main():
    opts = docopt(__doc__)
    tocfile = opts["<input_toc_file>"]
    runname = tocfile.split("_")[0]
    print(tocfile, runname)

if __name__ == "__main__":
    main()
