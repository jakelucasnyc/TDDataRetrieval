import logging
from Auth import Auth
from APIConnection import APIConnection

def main():
	logging.basicConfig(level=logging.INFO)
	log = logging.getLogger(__name__)


	authenticator = Auth()
	accessToken = authenticator.main()
	apiConn = APIConnection(accessToken)
	apiConn.getAccountsData()
	apiConn.getOptionsData()



if __name__ == "__main__":

	main()