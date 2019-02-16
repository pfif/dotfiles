from csv import DictReader
from datetime import datetime
from sys import argv, stderr

from converter import homebank_transaction, homebank_csv

# Unit : Convert TransferWise csv to transaction lines
def convert_creditmutuel_csv(itr):
    return [convert_line(line) for line in itr]


def convert_line(line):
    return homebank_transaction(
        datetime.strptime(line["Date de valeur"], "%d/%m/%Y"),
        amount(line),
        line["Libellé"]
    )


def amount(line):
    amount_raw = line["Débit"] if line["Débit"] else line["Crédit"]
    return float(amount_raw.replace(",", "."))

# Unit : Open transferwise file
def open_csv(filename):
    return DictReader(open(filename, 'r', newline='', encoding="latin_1"), delimiter=";")


if len(argv) == 2:
    print(homebank_csv(convert_creditmutuel_csv(open_csv(argv[1]))))
else:
    print("Usage: python3 %s filename" % argv[0], file=stderr)
