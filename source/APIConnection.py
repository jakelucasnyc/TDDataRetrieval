import logging
import requests

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class APIConnection:

	def __init__(self, accessToken):
		self.accessToken = accessToken
		self.authHeader = {
			'Authorization': 'Bearer ' + self.accessToken
		}

	def getAccountsData(self, positions=True, orders=True):

		fields = []
		if positions:
			fields.append('positions')
		if orders:
			fields.append('orders')

		if fields:
			params = {
				'fields': fields
			}
		else:
			params = None

		response = requests.get('https://api.tdameritrade.com/v1/accounts', headers=self.authHeader, params=params)
		responseJSON = response.json()
		log.debug(response.status_code)
		print(response.json())


	def getOptionsData(self):

		payload = {
			'includeQuotes': 'TRUE',
			'symbol': 'SPX',
			'contractType': 'PUT',
			'interval': 10,
			'strike': 3580,
			'strategy': 'VERTICAL',
			'daysToExpiration': 0
		}

		response = requests.get('https://api.tdameritrade.com/v1/marketdata/chains', headers=self.authHeader, params=payload)
		responseJSON = response.json()
		# print(responseJSON)


