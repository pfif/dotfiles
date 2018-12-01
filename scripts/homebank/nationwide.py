from pprint import pprint
from csv import DictReader
from datetime import datetime
from sys import argv, stderr

from converter import homebank_transaction, homebank_csv

# Unit : Convert TransferWise csv to transaction lines
def convert_nationwide_csv(itr):
    return [convert_line(line) for line in itr]


def convert_line(line):
    return homebank_transaction(
        datetime.strptime(line["Date"], "%d %b %Y"),
        amount(line),
        line["Description"]
    )

def amount(line):
    if line["Paid out"]:
        return 0 - pounds_to_float(line["Paid out"])
    return pounds_to_float(line["Paid in"])

def pounds_to_float(amount):
    return float(amount[1:])

# Unit : Open transferwise file
def open_csv(filename):
    file_ = open(filename, 'r', newline='\r\n', encoding="latin_1")

    while True:
        if file_.readline() == '\r\n':
            break

    return DictReader(file_)


if len(argv) == 2:
    print(homebank_csv(convert_nationwide_csv(open_csv(argv[1]))))
else:
    print("Usage: python3 %s filename" % argv[0], file=stderr)
