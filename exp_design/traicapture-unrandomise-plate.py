from __future__ import print_function
from csv import DictReader
from docopt import docopt
import sys
# python 2to3 hackery
try:
    xrange(1)
except NameError:
    xrange = range


__doc__ = """
USAGE:
    unrandomise.py -p <plate_csv> -d <db_csv>

"""

def _get_plate_tray_pos_dict(platefile):
    plate_fh = open(platefile)
    plate = DictReader(plate_fh)
    plate_dict = {}
    for row in plate:
        row_letter = row[""]  # it's a hack, but "" is the name of the 1st col
        for iii in xrange(1,13):
            col_num = str(iii)
            sample = row[col_num]
            if len(sample) < 2:
                continue
            # tuple of (chamber, pos)
            sys.stderr.write("%s %s\n" %( row_letter, col_num) )
            sample = (int(sample.split()[0]), sample.split()[1])
            sample_coord = row_letter + col_num
            plate_dict[sample_coord] = sample
    plate_fh.close()
    return plate_dict


def _get_tray_plant_id_dict(dbfile):
    db_fh = open(dbfile)
    db_csv = DictReader(db_fh)
    plant_dict = {}

    for plant_row in db_csv:
        # chamber id = chamber num - 1
        tray_pos = str(int(plant_row["experiment_location_id"]) + 1) + " " + plant_row["tray_position"]
        plant_dict[tray_pos] = plant_row
    db_fh.close()
    return plant_dict



def main():
    opts = docopt(__doc__)
    plate_dict = _get_plate_tray_pos_dict(opts["<plate_csv>"])
    plant_dict = _get_tray_plant_id_dict(opts["<db_csv>"])

    for pos, sample in plate_dict.iteritems():
        sample = "%i %s" % sample
        sample = sample.upper()
        plant = plant_dict[sample]["accession_id"]
        print("%s\t%s" % (pos, plant))

if __name__ == "__main__":
    main()
