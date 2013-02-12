from __future__ import print_function
from telnetlib import Telnet
from time import strptime, sleep, mktime
import datetime
import csv
import argparse

CSV_FIELDS = {
        "Date": 0,
        "Time": 1,
        "Temperature": 2,
        "Humidity": 3,
        "Light 1": 4,
        "Light 2": 5,
        "Light 3": 6,
        "Light 4": 7,
        }
SET_COMMAND = "pcoset"
DEVICE_ID = "0"  # as string
DATATYPES = {
        "Temperature": "I",
        "Humidity": "I",
        # Need info from Conviron for this
        "Light 1": "I",
        "Light 2": "I",
        "Light 3": "I",
        "Light 4": "I",
        } 
INDICIES = {
        "Temperature": 105,
        "Humidity": 106,
        # Need info from Conviron for this
        "Light 1": "107",
        "Light 2": "",
        "Light 3": "",
        "Light 4": "",
        }

STRP_FORMAT = "%m/%d/%Y %I:%M %p"

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
    parser.add_argument("-v", "--verbose", action="count", dest="verbosity",
            help="Verbosity level. The more -v's, the more verbose")
    parser.add_argument("-p", "--password", action="store", default="froot",
            help="The password of the user for the conviron", dest="passwd")
    return parser.parse_args()
    

def communicate_line(args, line):
    print("Communicating:", line)
    cmd_str = SET_COMMAND + " " + DEVICE_ID + " I "


    # Establish connection
    telnet = Telnet(args.host)
    response = telnet.read_until(b"login: ")
    if args.verbosity > 0:
        print(response)

    # Username
    payload = bytes(args.user + "\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"Password: ")
    if args.verbosity > 0:
        print(payload)
        print(response)
    
    # Password
    payload = bytes(args.passwd + "\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
 
    # PCOSET initialisation header
    payload = bytes(cmd_str + " 100 26\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
    
    payload = bytes(cmd_str + " 101 1\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
    
    payload = bytes(cmd_str + " 102 1\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
   
    # PCOSET send temperature
    payload = bytes(cmd_str + " 105 243\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
     
    # PCOSET send humidity
    payload = bytes(cmd_str + " 106 66\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
     
    # PCOSET send light 1
    payload = bytes(cmd_str + " 107 0\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)

    # PCOSET footer
    payload = bytes(cmd_str + " 123 1\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
     
    payload = bytes(cmd_str + " 121 1\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
     
    # Wait 3 seconds and clear write flag
    sleep(3)
    payload = bytes(cmd_str + " 120 0\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
 
    # Wait 3 seconds and force program reload
    sleep(3)
    payload = bytes(cmd_str + " 100 7\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
 
    payload = bytes(cmd_str + " 101 1\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
    payload = bytes(cmd_str + " 102 1\n", encoding="UTF8")

    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)

    payload = bytes(cmd_str + " 123 1\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
    
    payload = bytes(cmd_str + " 121 1\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
 
    # Wait 3 seconds and clear write flag
    sleep(3)
    payload = bytes(cmd_str + " 120 0\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
     
    # Wait 3 seconds, and clear busy flag
    sleep(3)
    payload = bytes(cmd_str + " 123 0\n", encoding="UTF8")
    telnet.write(payload)
    response = telnet.read_until(b"#")
    if args.verbosity > 0:
        print(payload)
        print(response)
     
    # Close telnet session
    telnet.close()
    
    
def main():
    args = get_args()
    
    csv_fh = open(args.csvfile, "rt")
    csv_reader = csv.reader(csv_fh, delimiter=',',
            quoting=csv.QUOTE_NONE)
    
    line = next(csv_reader)
    date_time = line[CSV_FIELDS["Date"]] + " " + line[CSV_FIELDS["Time"]]
    try:
        last_time = datetime.datetime.fromtimestamp(mktime(strptime(date_time, STRP_FORMAT)))
    except ValueError:
        line = next(csv_reader)
        date_time = line[CSV_FIELDS["Date"]] + " " + line[CSV_FIELDS["Time"]]
        last_time = datetime.datetime.fromtimestamp(mktime(strptime(date_time, STRP_FORMAT)))
    print(last_time)

# Ensure that the current date
    reached_now = False
    for line in csv_reader:
        date_time = line[CSV_FIELDS["Date"]] + " " + line[CSV_FIELDS["Time"]]
        time = datetime.datetime.fromtimestamp(mktime(strptime(date_time, STRP_FORMAT)))
        now = datetime.datetime.now()
        # use a window of 10 minutes to find current time in file
        timedelta = datetime.timedelta(minutes=10)
        #print(time, now)
        if time < now < time + timedelta:
            reached_now = True
            break
        elif time > now + timedelta:
            raise ValueError("The file starts too far into the future.")
    if not reached_now:
        raise ValueError("No date in the CSV file matches the current time.")
    
    line = next(csv_reader)
    date_time = line[CSV_FIELDS["Date"]] + " " + line[CSV_FIELDS["Time"]]
    last_time = datetime.datetime.fromtimestamp(mktime(strptime(date_time, STRP_FORMAT)))
    print(last_time)


    for line in csv_reader:
        date_time = line[CSV_FIELDS["Date"]] + " " + line[CSV_FIELDS["Time"]]
        time = datetime.datetime.fromtimestamp(mktime(strptime(date_time, STRP_FORMAT)))
        timediff = time - last_time
        last_time = time
        wait_sec = timediff.days * 24 * 60 * 60 + timediff.seconds
        print("Waiting %i secs." % wait_sec)
        sleep(0.0001)
        #sleep(wait_sec)
        communicate_line(args, line)

if __name__ == "__main__":
    main()
