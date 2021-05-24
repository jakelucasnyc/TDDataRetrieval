import logging
from auth import Auth
from apiConnection import APIConnection
from parse.transactionHistory import TransactionHistoryParse
from dbConnection import DBConnection

def main():
	logging.basicConfig(level=logging.INFO)
	log = logging.getLogger(__name__)

	dbConn = DBConnection()
	authenticator = Auth()
	accessToken = authenticator.main()
	apiConn = APIConnection(authenticator, accessToken)
	# transactions = apiConn.getTransactionHistory(startDate='2021-01-01')
	# for transaction in transactions:
	# 	dbConn.insertTransaction(transaction)

	acctData = apiConn.getAccountsData()



if __name__ == "__main__":

	main()