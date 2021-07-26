import logging
import requests
from appSecrets import secrets
from parse import TransactionHistoryParse, PositionsParse, AccountParse

log = logging.getLogger(__name__)

class APIConnection:

  def __init__(self, authenticator, accessToken):
    self.authenticator = authenticator
    self.accessToken = accessToken
    self.authHeader = {
      'Authorization': 'Bearer ' + self.accessToken
    }

  def getAccountsData(self, positions=False):

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
    if response.status_code == 200:
      responseJSON = response.json()
      accounts = []
      positions = []
      balances = []
      for acct in responseJSON:
        # print(acct['securitiesAccount']['initialBalances'], end='\n\n')
        balances.append(acct['securitiesAccount']['currentBalances'])
        if 'positions' in acct['securitiesAccount'].keys():
          positionParser = PositionsParse(acct)	
          positions.append(positionParser.main())
        # accountParser = AccountParse(acct)
        # accounts.append(accountParser.main())

      firstKeys = balances[0].keys()
      remainingKeys = []
      for balance in balances[1:]:
        remainingKeys.append(set(balance.keys()))
      commonKeys = [key for key in set(firstKeys).intersection(*remainingKeys)]
      # print(commonKeys)
      for balance in balances:
        print({key: value for key, value in balance.items() if not key in commonKeys}, end='\n\n')
      return accounts, positions, balances

    else:
      log.error(f'Unable to get account data. Status Code : {response.status_code}')
      return None


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

    if response.status_code == 200:
      responseJSON = response.json()

    else:
      log.warning(f'Unable to get options data. Status Code: {response.status_code}')
    # print(responseJSON)

  def getTransactionHistory(self, startDate=None, symbol=None):

    payload = {
      'type': 'ALL',
      'symbol': symbol,
      'startDate': startDate,

    }

    response = requests.get(f'https://api.tdameritrade.com/v1/accounts/{secrets.ACCOUNT_ID}/transactions', headers=self.authHeader, params=payload)
    parsedTransactions = []

    if response.status_code == 200:
      responseJSON = response.json()
      # for response in responseJSON:
      # 	print(str(response)+'\n\n\n')
      
      for transaction in responseJSON:
        parsedTransaction = TransactionHistoryParse(transaction).main()
        parsedTransactions.append(parsedTransaction)
    else:
      log.critical(f'Failed to Retrieve Data. Status Code: {response.status_code}')

    return parsedTransactions

    



