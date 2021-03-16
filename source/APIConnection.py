import logging
import requests
import secrets

log = logging.getLogger(__name__)

class APIConnection:

	def __init__(self, authenticator, accessToken):
		self.authenticator = authenticator
		self.accessToken = accessToken
		self.authHeader = {
			'Authorization': 'Bearer ' + self.accessToken
		}

	def getAccountsData(self, positions=True):

		fields = []
		if positions:
			fields.append('positions')

		if fields:
			payload = {
				'fields': fields
			}
		else:
			payload = None

		response = requests.get('https://api.tdameritrade.com/v1/accounts', headers=self.authHeader, params=payload)
		responseJSON = response.json()
		log.debug(response.status_code)
		return responseJSON


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

	def getTransactionHistory(self, startDate=None, symbol=None):

		payload = {
			'type': 'TRADE',
			'symbol': symbol,
			'startDate': startDate,

		}

		response = requests.get(f'https://api.tdameritrade.com/v1/accounts/{secrets.ACCOUNT_ID}/transactions', headers=self.authHeader, params=payload)
		responseJSON = response.json()
		return responseJSON[0]


	def main(self):

		return self.getTransactionHistory(symbol='RGR', startDate='2021-01-01')



