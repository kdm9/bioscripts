from __future__ import print_function
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
DEVICE_ID = "0"
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
    parser.add_argument("-c", "--csv-file", action="store", required=False,
            help="The CSV file describing the environmental conditions",
            dest="csvfile")
    parser.add_argument("-u", "--user", action="store", default=b"root\n",
            help="The login username for the conviron", dest="user")
    parser.add_argument("-p", "--password", action="store", default=b"froot\n",
            help="The password of the user for the conviron", dest="passwd")
    return parser.parse_args()
    

def communicate_line(args, line):
    cmd_str = b"pcoset 0 I"
    telnet = Telnet(args.host)
    print(telnet.read_until(b"login: "))
    telnet.write(args.user)
    print(telnet.read_until(b"Password: "))
    telnet.write(args.passwd)
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 100 26\n")
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 101 1\n")
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 102 1\n")
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 105 243\n")
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 106 66\n")
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 123 1\n")
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 121 1\n")
    
    sleep(3)
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 120 0\n")

    sleep(3)
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 100 7\n")
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 101 1\n")
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 102 1\n")
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 123 1\n")
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 121 1\n")
    
    sleep(3)
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 120 0\n")
    
    sleep(3)
    print(telnet.read_until(b"#"))
    telnet.write(cmd_str + b" 123 0\n")
    telnet.close()
    
    
def main():
    args = get_args()
    communicate_line(args, None)
    return
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

if __name__ == "__main__":
    main()