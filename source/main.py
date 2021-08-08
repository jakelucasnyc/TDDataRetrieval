import logging
from auth import Auth
from apiConnection import APIConnection
from parse.transactions import TransactionHistoryParse
from db import DBConnection

def main():
    # logging.basicConfig(filename='../app.log', format='%(asctime)s - %(levelname)s:%(name)s -> %(message)s', level=logging.INFO)
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    log.info('Application started')

    dbConn = DBConnection()
    authenticator = Auth()
    accessToken = authenticator.main()
    apiConn = APIConnection(authenticator, accessToken)
    for yearDiff in range(10, 21):
        year = 2000 + yearDiff 
        print(year)

        transactions = apiConn.getTransactionHistory(startDate=f'{year}-01-01')
        for transaction in transactions:
            dbConn.insert(transaction)
        log.info('Inserted transactions')
        # break
    # accts, positions, balances = apiConn.getAccountsData()



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception('Program Crashed')