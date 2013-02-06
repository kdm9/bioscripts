from telnetlib import Telnet
from time import strptime, sleep
import datetime
import csv
import argparse

CSV_FIELDS = {
        "Date": 0,
        "Time": 1,
        "Temperature": 2,
        "Humidity": 3,
        }
COMMAND = "pcoset"
DEVICE_ID = 0
MODE = "I"
INDICIES = {
        "Temperature": 105,
        "Humidity": 106,
        }


def get_args():
    parser = argparse.ArgumentParser(description="Daemon to update"
            " environmental conditions of Conviron cabinets in real time")
    parser.add_argument("-H", "--host", action="store", required=True,
            help="Host of the Conviron, to Telnet into", dest="host")
    parser.add_argument("-c", "--csv-file", action="store", required=True,
            help="The CSV file describing the environmental conditions",
            dest="csvfile")
    parser.add_argument("-u", "--user", action="store", default="root",
            help="The login username for the conviron", dest="user")
    parser.add_argument("-p", "--password", action="store", default="froot",
            help="The password of the user for the conviron", dest="passwd")
    return parser.parse_args()
    

def communicate_line(args, line):
    telnet = Telnet(args.host)



def main():
    args = get_args()
    csv_fh = open(args.csvfile, "rt")
    csv_reader = csv.reader(csv_fh, delimiter=',',
            header=False, quoting=csv.QUOTE_NONE)
    
    line = csv_reader.next()
    date_time = line[CSV_FIELDS["Date"]] + " " + line[CSV_FIELDS["Time"]]
    last_time = strptime(date_time, "%m/%d/%Y %I:%M %p")
    communicate_line(args, line)

    for line in csv_reader:
        date_time = line[CSV_FIELDS["Date"]] + " " + line[CSV_FIELDS["Time"]]
        time = strptime(date_time, "%m/%d/%Y %I:%M %p")
        timediff = time - last_time
        last_time = time
        wait_sec = timediff.days * 24 * 60 * 60 + timediff.seconds
        sleep(wait_sec)
        communicate_line(args, line)


        



