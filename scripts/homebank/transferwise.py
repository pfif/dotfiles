from csv import DictReader
from datetime import datetime
from sys import argv, stderr

from converter import homebank_transaction, homebank_csv

# Unit : Convert TransferWise csv to transaction lines
def convert_transferwise_csv(itr):
    return [convert_line(line) for line in itr]


def convert_line(line):
    return homebank_transaction(
        datetime.strptime(line["Date"], "%d-%m-%Y"),
        float(line["Amount"]),
        info(line)
    )


def info(line):
    if line["Payee Name"]:
        return "%s - %s" % (line["Payee Name"], line["Payment Reference"])
    return line["Merchant"]

# Unit : Open transferwise file
def open_csv(filename):
    return DictReader(open(filename, 'r', newline=''))


if len(argv) == 2:
    print(homebank_csv(convert_transferwise_csv(open_csv(argv[1]))))
else:
    print("Usage: python3 %s filename" % argv[0], file=stderr)
