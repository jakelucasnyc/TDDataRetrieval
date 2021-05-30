import logging
from auth import Auth
from apiConnection import APIConnection
from parse.transactions import TransactionHistoryParse
from db import DBConnection

def main():
    logging.basicConfig(filename='../app.log', format='%(asctime)s - %(levelname)s:%(name)s -> %(message)s', level=logging.INFO)
    log = logging.getLogger(__name__)

    log.info('Application started')

    dbConn = DBConnection()
    authenticator = Auth()
    accessToken = authenticator.main()
    apiConn = APIConnection(authenticator, accessToken)
    transactions = apiConn.getTransactionHistory(startDate='2021-04-01')
    for transaction in transactions:
        dbConn.insert(transaction)
    log.info('Inserted transactions')
    acctData = apiConn.getAccountsData(True)



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception('Program Crashed')