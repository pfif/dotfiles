from csv import DictReader
from datetime import datetime
from sys import argv, stderr

from converter import homebank_transaction, homebank_csv

# Unit : Convert TransferWise csv to transaction lines
def convert_creditmutuel_csv(itr):
    return [convert_line(line) for line in itr]


def convert_line(line):
    return homebank_transaction(
        datetime.strptime(line["Datum"], "%Y%m%d"),
        amount(line),
        line["Naam / Omschrijving"]
    )


def amount(line):
    amount = float(line["Bedrag (EUR)"].replace(",","."))
    if line["Af Bij"] == "Af":
        return 0 - amount
    return amount

# Unit : Open transferwise file
def open_csv(filename):
    return DictReader(open(filename, 'r', newline='', encoding="latin_1"))


if len(argv) == 2:
    print(homebank_csv(convert_creditmutuel_csv(open_csv(argv[1]))))
else:
    print("Usage: python3 %s filename" % argv[0], file=stderr)
