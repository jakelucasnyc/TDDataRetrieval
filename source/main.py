import logging
from auth import Auth
from apiConnection import APIConnection
from parse import transactionHistory

def main():
	logging.basicConfig(level=logging.INFO)
	log = logging.getLogger(__name__)


	authenticator = Auth()
	accessToken = authenticator.main()
	apiConn = APIConnection(authenticator, accessToken)
	dataDict = apiConn.main()
	parser = transactionHistory.TransactionHistoryParse(dataDict)
	parser.main()



if __name__ == "__main__":

	main()