from parse.base import Base
import logging
import json
import datetime

log = logging.getLogger(__name__)
class TransactionHistoryParse(Base):

	def __init__(self, dataDict: dict):
		super().__init__(dataDict)
		self.totalFees = 0.00
		for value in self.fees.values():
			self.totalFees += value

	@staticmethod
	def _datetimeStrToBetterStr(datetimeStr):
		obj = datetime.datetime.strptime(datetimeStr, '%Y-%m-%dT%H:%M:%S+0000')
		return obj.strftime('%Y-%m-%d %H:%M:%S')
		

	def collectNecessaryData(self):

		parsedDict = {}

		try:

			if self.type == 'TRADE':

				if self.transactionItem['instrument']['assetType'] == 'OPTION':
					addedData = {
						'table': 'trade_transactions',
						'type': self.type,
						'transaction_date': TransactionHistoryParse._datetimeStrToBetterStr(self.transactionDate),
						'settlement_date': self.settlementDate,
						'transaction_id': self.transactionId,
						'account_id': self.transactionItem['accountId'],
						'expiration_date': TransactionHistoryParse._datetimeStrToBetterStr(self.transactionItem['instrument']['optionExpirationDate']),
						'ticker': self.transactionItem['instrument']['underlyingSymbol'],
						'symbol': self.transactionItem['instrument']['symbol'],
						'cusip': self.transactionItem['instrument']['cusip'],
						'put_or_call': self.transactionItem['instrument']['putCall'],
						'quantity_contracts': self.transactionItem['amount'],
						'cost': self.transactionItem['cost'],
						'total_fees': self.totalFees,
						'fees_dict': json.dumps(self.fees),
						'net_amount': self.netAmount,
						'price_per_share': self.transactionItem['price'],
						'instruction': self.transactionItem['instruction'],
						'instrument_description': self.transactionItem['instrument']['description'],
						'asset_type': self.transactionItem['instrument']['assetType'],
						'transaction_subtype': self.transactionSubType,
						'description': self.description
					}
					parsedDict.update(addedData)

				elif self.transactionItem['instrument']['assetType'] == 'EQUITY':

					addedData = {
						'table': 'trade_transactions',
						'type': self.type,
						'transaction_date': TransactionHistoryParse._datetimeStrToBetterStr(self.transactionDate),
						'settlement_date': self.settlementDate,
						'transaction_id': self.transactionId,
						'account_id': self.transactionItem['accountId'],
						# 'expiration_date': self.transactionItem['instrument']['optionExpirationDate'],
						'ticker': self.transactionItem['instrument']['symbol'],
						'symbol': self.transactionItem['instrument']['symbol'],
						'cusip': self.transactionItem['instrument']['cusip'],
						# 'put_or_call': self.transactionItem['instrument']['putCall'],
						'quantity_shares': self.transactionItem['amount'],
						'cost': self.transactionItem['cost'],
						'total_fees': self.totalFees,
						'fees_dict': json.dumps(self.fees),
						'net_amount': self.netAmount,
						'price_per_share': self.transactionItem['price'],
						'instruction': self.transactionItem['instruction'],
						# 'instrument_description': self.transactionItem['instrument']['description'],
						'asset_type': self.transactionItem['instrument']['assetType'],
						'transaction_subtype': self.transactionSubType,
						'description': self.description
					}
					parsedDict.update(addedData)

			elif self.type == 'DIVIDEND_OR_INTEREST':

				addedData = {
					'table': 'dividend_or_interest_transactions',
					'type': self.type,
					'settlement_date': self.settlementDate,
					'net_amount': self.netAmount,
					'transaction_date': TransactionHistoryParse._datetimeStrToBetterStr(self.transactionDate),
					'transaction_subtype': self.transactionSubType,
					'transaction_id': self.transactionId,
					'description': self.description,
					'total_fees': self.totalFees,
					'fees_dict': json.dumps(self.fees),
					'account_id': self.transactionItem['accountId'],
					'cost': self.transactionItem['cost']
				}
				parsedDict.update(addedData)

			elif self.type == 'RECEIVE_AND_DELIVER':

				if self.transactionItem['instrument']['assetType'] == 'OPTION':

					addedData = {
						'table': 'receive_and_deliver_transactions',
						'type': self.type,
						'settlement_date': self.settlementDate,
						'net_amount': self.netAmount,
						'transaction_date': TransactionHistoryParse._datetimeStrToBetterStr(self.transactionDate),
						'transaction_subtype': self.transactionSubType,
						'transaction_id': self.transactionId,
						'description': self.description,
						'total_fees': self.totalFees,
						'fees_dict': json.dumps(self.fees),
						'account_id': self.transactionItem['accountId'],
						'cost': self.transactionItem['cost'],
						'expiration_date': TransactionHistoryParse._datetimeStrToBetterStr(self.transactionItem['instrument']['optionExpirationDate']),
						'cusip': self.transactionItem['instrument']['cusip'],
						'asset_type': self.transactionItem['instrument']['assetType'],
						'quantity_contracts': self.transactionItem['amount']

					}

				elif self.transactionItem['instrument']['assetType'] == 'CASH_EQUIVALENT':

					addedData = {
						'table': 'receive_and_deliver_transactions',
						'type': self.type,
						'settlement_date': self.settlementDate,
						'net_amount': self.netAmount,
						'transaction_date': TransactionHistoryParse._datetimeStrToBetterStr(self.transactionDate),
						'transaction_subtype': self.transactionSubType,
						'transaction_id': self.transactionId,
						'description': self.description,
						'total_fees': self.totalFees,
						'fees_dict': json.dumps(self.fees),
						'account_id': self.transactionItem['accountId'],
						'cost': self.transactionItem['cost'],
						# 'expiration_date': self.transactionItem['instrument']['optionExpirationDate'],
						'cusip': self.transactionItem['instrument']['cusip'],
						'symbol': self.transactionItem['instrument']['symbol'],
						'asset_type': self.transactionItem['instrument']['assetType'],
						'instrument_type': self.transactionItem['instrument']['type'],

						# 'quantity_contracts': self.transactionItem['amount']

					}
				parsedDict.update(addedData)

			elif self.type == 'JOURNAL':
				
				addedData = {
					'table': 'journal_transactions',
					'type': self.type,
					'settlement_date': self.settlementDate,
					'net_amount': self.netAmount,
					'transaction_date': TransactionHistoryParse._datetimeStrToBetterStr(self.transactionDate),
					'transaction_subtype': self.transactionSubType,
					'transaction_id': self.transactionId,
					'description': self.description,
					'total_fees': self.totalFees,
					'fees_dict': json.dumps(self.fees),
					'account_id': self.transactionItem['accountId'],
					'cost': self.transactionItem['cost']
				}

				if hasattr(self, 'clearingReferenceNumber'):
					addedData.update({'clearing_reference_number': self.clearingReferenceNumber})

				if hasattr(self, 'achStatus'):
					addedData.update({'ach_status': self.achStatus})

				parsedDict.update(addedData)

			elif self.type == 'ELECTRONIC_FUND':

				addedData = {
					'table': 'electronic_fund_transactions',
					'type': self.type,
					'settlement_date': self.settlementDate,
					'net_amount': self.netAmount,
					'transaction_date': TransactionHistoryParse._datetimeStrToBetterStr(self.transactionDate),
					'transaction_subtype': self.transactionSubType,
					'transaction_id': self.transactionId,
					'description': self.description,
					'total_fees': self.totalFees,
					'fees_dict': json.dumps(self.fees),
					'account_id': self.transactionItem['accountId'],
					'cost': self.transactionItem['cost']
				}
				parsedDict.update(addedData)

			else:
				log.warning('Unknown Transaction Type')
				print('\n\n', self.dataDict, '\n\n')

		except (KeyError, AttributeError) as e:
			log.critical(f'Key or Attribute not found in data. Must change data categorization logic.\nError: {e}')
			print('\n\n', self.dataDict, '\n\n')

		else:
			log.debug('Successful Data Parsing')

		finally:

			return parsedDict

	def main(self):

		return self.collectNecessaryData()

		


	