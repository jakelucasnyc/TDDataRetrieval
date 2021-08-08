import logging
import json
import datetime

log = logging.getLogger(__name__)
class TransactionHistoryParse():

	def __init__(self, dataDict: dict):
		self.dataDict = dataDict
		self.totalFees = 0.00
		for value in self.dataDict['fees'].values():
			self.totalFees += value

	@staticmethod
	def _datetimeStrToBetterStr(datetimeStr):
		obj = datetime.datetime.strptime(datetimeStr, '%Y-%m-%dT%H:%M:%S+0000')
		return obj.strftime('%Y-%m-%d %H:%M:%S')
		

	def collectNecessaryData(self):

		parsedDict = {}

		try:

			if self.dataDict['type'] == 'TRADE':

				if self.dataDict['transactionItem']['instrument']['assetType'] == 'OPTION':
					addedData = {
						'table': 'trade_transactions',
						'type': self.dataDict['type'],
						'transaction_date': TransactionHistoryParse._datetimeStrToBetterStr(self.dataDict['transactionDate']),
						'settlement_date': self.dataDict['settlementDate'],
						'transaction_id': self.dataDict['transactionId'],
						'account_id': self.dataDict['transactionItem']['accountId'],
						'expiration_date': TransactionHistoryParse._datetimeStrToBetterStr(self.dataDict['transactionItem']['instrument']['optionExpirationDate']),
						'ticker': self.dataDict['transactionItem']['instrument']['underlyingSymbol'],
						'symbol': self.dataDict['transactionItem']['instrument']['symbol'],
						'cusip': self.dataDict['transactionItem']['instrument']['cusip'],
						'put_or_call': self.dataDict['transactionItem']['instrument']['putCall'],
						'quantity_contracts': self.dataDict['transactionItem']['amount'],
						'cost': self.dataDict['transactionItem']['cost'],
						'total_fees': self.totalFees,
						'fees_dict': json.dumps(self.dataDict['fees']),
						'net_amount': self.dataDict['netAmount'],
						'price_per_share': self.dataDict['transactionItem']['price'],
						'instruction': self.dataDict['transactionItem']['instruction'],
						'instrument_description': self.dataDict['transactionItem']['instrument']['description'],
						'asset_type': self.dataDict['transactionItem']['instrument']['assetType'],
						'transaction_subtype': self.dataDict['transactionSubType'],
						'description': self.dataDict['description']
					}
					parsedDict.update(addedData)

				elif self.dataDict['transactionItem']['instrument']['assetType'] == 'EQUITY':

					addedData = {
						'table': 'trade_transactions',
						'type': self.dataDict['type'],
						'transaction_date': TransactionHistoryParse._datetimeStrToBetterStr(self.dataDict['transactionDate']),
						'settlement_date': self.dataDict['settlementDate'],
						'transaction_id': self.dataDict['transactionId'],
						'account_id': self.dataDict['transactionItem']['accountId'],
						# 'expiration_date': self.transactionItem['instrument']['optionExpirationDate'],
						'symbol': self.dataDict['transactionItem']['instrument']['symbol'],
						'cusip': self.dataDict['transactionItem']['instrument']['cusip'],
						# 'put_or_call': self.dataDict['transactionItem']['instrument']['putCall'],
						'quantity_contracts': self.dataDict['transactionItem']['amount'],
						'cost': self.dataDict['transactionItem']['cost'],
						'total_fees': self.totalFees,
						'fees_dict': json.dumps(self.dataDict['fees']),
						'net_amount': self.dataDict['netAmount'],
						'price_per_share': self.dataDict['transactionItem']['price'],
						'instruction': self.dataDict['transactionItem']['instruction'],
						# 'instrument_description': self.dataDict['transactionItem']['instrument']['description'],
						'asset_type': self.dataDict['transactionItem']['instrument']['assetType'],
						'transaction_subtype': self.dataDict['transactionSubType'],
						'description': self.dataDict['description']
					}
					parsedDict.update(addedData)

					if 'underlyingSymbol' in self.dataDict['transactionItem']['instrument'].keys():
						parsedDict.update({'ticker': self.dataDict['transactionItem']['instrument']['underlyingSymbol']})

			elif self.dataDict['type'] == 'DIVIDEND_OR_INTEREST':

				addedData = {
					'table': 'dividend_or_interest_transactions',
					'type': self.dataDict['type'],
					'settlement_date': self.dataDict['settlementDate'],
					'net_amount': self.dataDict['netAmount'],
					'transaction_date': TransactionHistoryParse._datetimeStrToBetterStr(self.dataDict['transactionDate']),
					'transaction_subtype': self.dataDict['transactionSubType'],
					'transaction_id': self.dataDict['transactionId'],
					'description': self.dataDict['description'], 
					'total_fees': self.totalFees,
					'fees_dict': json.dumps(self.dataDict['fees']),
					'account_id': self.dataDict['transactionItem']['accountId'],
					'cost': self.dataDict['transactionItem']['cost'],
				}
				parsedDict.update(addedData)

			elif self.dataDict['type'] == 'RECEIVE_AND_DELIVER':

				if self.dataDict['transactionItem']['instrument']['assetType'] == 'OPTION':

					addedData = {
						
						'table': 'receive_and_deliver_transactions',
						'type': self.dataDict['type'],
						'settlement_date': self.dataDict['settlementDate'],
						'net_amount': self.dataDict['netAmount'],
						'transaction_date': TransactionHistoryParse._datetimeStrToBetterStr(self.dataDict['transactionDate']),
						'transaction_subtype': self.dataDict['transactionSubType'],
						'transaction_id': self.dataDict['transactionId'],
						'description': self.dataDict['description'], 
						'total_fees': self.totalFees,
						'fees_dict': json.dumps(self.dataDict['fees']),
						'account_id': self.dataDict['transactionItem']['accountId'],
						'cost': self.dataDict['transactionItem']['cost'],
						'expiration_date': TransactionHistoryParse._datetimeStrToBetterStr(self.dataDict['transactionItem']['instrument']['optionExpirationDate']),
						'cusip': self.dataDict['transactionItem']['instrument']['cusip'],
						'asset_type': self.dataDict['transactionItem']['instrument']['assetType'],
						'quantity_contracts': self.dataDict['transactionItem']['amount']

					}

				elif self.dataDict['transactionItem']['instrument']['assetType'] == 'CASH_EQUIVALENT':

					addedData = {
						'table': 'receive_and_deliver_transactions',
						'type': self.dataDict['type'],
						'settlement_date': self.dataDict['settlementDate'],
						'net_amount': self.dataDict['netAmount'],
						'transaction_date': TransactionHistoryParse._datetimeStrToBetterStr(self.dataDict['transactionDate']),
						'transaction_subtype': self.dataDict['transactionSubType'],
						'transaction_id': self.dataDict['transactionId'],
						'description': self.dataDict['description'], 
						'total_fees': self.totalFees,
						'fees_dict': json.dumps(self.dataDict['fees']),
						'account_id': self.dataDict['transactionItem']['accountId'],
						'cost': self.dataDict['transactionItem']['cost'],
						# 'expiration_date': TransactionHistoryParse._datetimeStrToBetterStr(self.dataDict['transactionItem']['instrument']['optionExpirationDate']),
						'cusip': self.dataDict['transactionItem']['instrument']['cusip'],
						'asset_type': self.dataDict['transactionItem']['instrument']['assetType'],
						# 'quantity_contracts': self.dataDict['transactionItem']['instrument']['amount']
					}
				parsedDict.update(addedData)

			elif self.dataDict['type'] == 'JOURNAL':
				
				addedData = {
					'table': 'journal_transactions',
					'type': self.dataDict['type'],
					'settlement_date': self.dataDict['settlementDate'],
					'net_amount': self.dataDict['netAmount'],
					'transaction_date': TransactionHistoryParse._datetimeStrToBetterStr(self.dataDict['transactionDate']),
					'transaction_subtype': self.dataDict['transactionSubType'],
					'transaction_id': self.dataDict['transactionId'],
					'description': self.dataDict['description'], 
					'total_fees': self.totalFees,
					'fees_dict': json.dumps(self.dataDict['fees']),
					'account_id': self.dataDict['transactionItem']['accountId'],
					'cost': self.dataDict['transactionItem']['cost'],
				}

				if hasattr(self, 'clearingReferenceNumber'):
					addedData.update({'clearing_reference_number': self.dataDict['clearingReferenceNumber']})

				if hasattr(self, 'achStatus'):
					addedData.update({'ach_status': self.dataDict['achStatus']})

				parsedDict.update(addedData)

			elif self.dataDict['type'] == 'ELECTRONIC_FUND':

				addedData = {
					'table': 'electronic_fund_transactions',
					'type': self.dataDict['type'],
					'settlement_date': self.dataDict['settlementDate'],
					'net_amount': self.dataDict['netAmount'],
					'transaction_date': TransactionHistoryParse._datetimeStrToBetterStr(self.dataDict['transactionDate']),
					'transaction_subtype': self.dataDict['transactionSubType'],
					'transaction_id': self.dataDict['transactionId'],
					'description': self.dataDict['description'], 
					'total_fees': self.totalFees,
					'fees_dict': json.dumps(self.dataDict['fees']),
					'account_id': self.dataDict['transactionItem']['accountId'],
					'cost': self.dataDict['transactionItem']['cost'],
				}
				parsedDict.update(addedData)

			else:
				log.warning(f'Unknown Transaction Type\n\n{self.dataDict}\n\n')
				# print('\n\n', self.dataDict, '\n\n')

		except (KeyError) as e:
			log.exception(f'Key or Attribute not found in data. Must change data categorization logic.\nError: {e}\nDataDict: {self.dataDict}')
			# print('\n\n', self.dataDict, '\n\n')
			parsedDict = {}

		else:
			log.debug('Successful Data Parsing')

		finally:

			return parsedDict

	def main(self):

		return self.collectNecessaryData()

		


	