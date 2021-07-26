import logging

log = logging.getLogger(__name__)

class AccountParse:
    
  def __init__(self, dataDict):
    self.dataDict = dataDict
    self.acct = self.dataDict['securitiesAccount']
    self.initialBalances = self.acct['initialBalances']
    self.currentBalances = self.acct['currentBalances']

      
  def _getData(self):
    try:
      parsedAcct = {
        'table': 'accounts',
        'type': self.acct['type'],
        'account_id': self.acct['accountId'],
        'round_trips': self.acct['roundTrips'],
        'is_day_trader': self.acct['isDayTrader'],
        'is_closing_only_restricted': self.acct['isClosingOnlyRestricted'],
        
      }
    except KeyError as e:
      log.exception(f'Error in AccountParse._getData(): {e}\nData Dict: {self.dataDict}\n')
      return None
    else:
      return parsedAcct

  def main(self):
    return self._getData()