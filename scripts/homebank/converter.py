from csv import writer
from io import StringIO


# Unit : Make a transaction line
def homebank_transaction(date, amount, info):
    return [
        date.strftime("%m-%d-%y"),
        0,
        info,
        '',
        '',
        amount,
        '',
        ''
    ]


# Unit : Make homebank file
def homebank_csv(homebank_transactions):
    csv = StringIO()
    homebank_writer = writer(csv, delimiter=";")
    homebank_writer.writerows(homebank_transactions)

    return csv.getvalue()

