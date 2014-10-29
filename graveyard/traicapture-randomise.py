from __future__ import print_function
from random import randrange
from json import load, dump
from docopt import docopt
from os.path import exists
import os

__doc__ = """
traitcapture-randomise

USAGE:
    traitcapture-randomise -c <chambersize> -j <jsonfile> -n <numpots> -t <traytype> -x <skippos>

OPTIONS:
    -c <chambersize>	Number of pots in the chamber
    -j <jsonfile>		Json file containing remaining pots.
    -n <numpots>		Allocate this number of pots
    -t <traytype>       One of: none, 5x4 (old way), 4x5 (trayscan/new way)
    -x <skippos>        Comma separated list of tray positions to skip
"""

TRAYS = {
        "5x4": [
            'A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'C1', 'C2', 'C3', 'C4',
            'D1', 'D2', 'D3', 'D4', 'E1', 'E2', 'E3', 'E4',
            ],
        "4x5": [
            'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'C1', 'C2',
            'C3', 'C4', 'C5', 'D1', 'D2', 'D3', 'D4', 'D5',
            ],
        "none": ["",]
        }

def make_chamber(tray_type, chamber_size,skip):
    """Given a chamber size, and tray type, this creates a list of chamber
    positions"""

    tray_size = len(TRAYS[tray_type])
    if chamber_size % tray_size  != 0:
        raise ValueError("Not a round number of trays per chamber. chamber"
                "size %% tray size == %i" % chamber_size % tray_size)
    chamber = []
    for iii in xrange(chamber_size):
        tray_idx = (iii % tray_size) + 1
        if tray_idx == 0:
            tray_idx = tray_size
        if tray_idx in skip:
            continue
        traypos = str(iii//tray_size+1) + TRAYS[tray_type][iii%tray_size]
        chamber.append((iii + 1, traypos))
    return chamber

if __name__ == "__main__":
    opts = docopt(__doc__)

    chamber_size = int(opts["-c"])
    numtopop = int(opts["-n"])
    skip = [int(x) for x in opts["-x"].split(",")]
    json_file = opts["-j"]
    tray_type = opts["-t"]


    # Get chamber position list from file
    try:
        j_fh = open(json_file)
        chamber = load(j_fh)["remaining"]
        if len(chamber) < 1:
            raise ValueError
    except (ValueError, IOError):
        chamber = make_chamber(tray_type, chamber_size, skip)

    # Check we can actually pop the right number
    if len(chamber) < numtopop:
        raise ValueError("Can't allocate %i numtopop. Only %i pots left in"
                "chamber" % (numtopop, len(chamber)))

    for iii in xrange(numtopop):
        posnum, posname = chamber.pop(randrange(len(chamber)))
        print("%s\t%s" % (posnum, posname))

    if len(chamber) > 0:
        try:
            j_fh.close()
        except NameError:
            pass
        j_fh = open(json_file, "w")
        dump({"remaining": chamber}, j_fh)
        j_fh.close()
    else:
        try:
            os.remove(json_file)
        except OSError:
            pass
