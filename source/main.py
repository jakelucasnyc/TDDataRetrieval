import logging
from Auth import Auth
from APIConnection import APIConnection
from Parse import TransactionHistory

def main():
	logging.basicConfig(level=logging.INFO)
	log = logging.getLogger(__name__)


	authenticator = Auth()
	accessToken = authenticator.main()
	apiConn = APIConnection(authenticator, accessToken)
	dataDict = apiConn.main()
	parser = TransactionHistory.TransactionHistoryParse(dataDict)
	parser.main()



if __name__ == "__main__":

	main()