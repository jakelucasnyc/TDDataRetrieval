import logging

log = logging.getLogger(__name__)

class BalanceBase:
  def __init__(self, dataDict):
    self.dataDict = dataDict

  def _getCommonInitialData(self):
    balances = self.dataDict['initialBalances'] 

    returnDict = {
      'accruedInterest': balances['accruedInterest'],
      'cash_available_for_trading': balances['cashAvailableForTrading'],
      'cash_balance': balances['cashBalance'],
      'bond_value': balances['bondValue'],
      'cash_receipts': balances['cashReceipts'],
      'liquidation_value': balances['liquidationValue'],
      'long_option_market_value': balances['longOptionMarketValue'],
      'long_stock_value': balances['longStockValue'],
      'money_market_fund': balances['moneyMarketFund'],
      'mutual_fund_value': balances['mutualFundValue'],
      'short_option_market_value': balances['shortOptionMarkeyValue'],
      'short_stock_value': balances['shortStockValue'],
      'is_in_call': balances['isInCall'],
      'pending_deposits': balances['pendingDeposits'],
      'account_value': balances['accountValue'],
           
    }
    return returnDict

  def _getCommonCurrentData(self):
    balances = self.dataDict['currentBalances']

    returnDict = {
      'accruedInterest': balances['accruedInterest'],
      'cash_balance': balances['cashBalance'],
      'bond_value': balances['bondValue'],
      'cash_receipts': balances['cashReceipts'],
      'liquidation_value': balances['liquidationValue'],
      'long_option_market_value': balances['longOptionMarketValue'],
      'long_market_value': balances['longStockValue'],
      'money_market_fund': balances['moneyMarketFund'],
      'mutual_fund_value': balances['mutualFundValue'],
      'short_option_market_value': balances['shortOptionMarkeyValue'],
      'short_market_value': balances['shortStockValue'],
      'pending_deposits': balances['pendingDeposits'],
      'savings': balances['savings']

    }

class CashInitialBalancesParse(BalanceBase):
  def __init__(self, dataDict):
    super().__init__(dataDict)
    self.dataDict = dataDict
    self.commonData = self._getCommonInitialData()

  def _getData(self):
    self.commonData.update({
      'cash_available_for_withdrawal': self.dataDict['initalBalances']['cashAvailableForWithdrawal'],
      'unsettled_cash': self.dataDict['initalBalances']['unsettledCash'],
      'cash_debit_call_value': self.dataDict['initalBalances']['cashDebitCallValue']
    })

class CashCurrentBalancesParse(BalanceBase):
  def __init__(self, dataDict):
    super().__init__(dataDict)
    self.dataDict = dataDict
    self.commonData = self._getCommonCurrentData()

  def _getData(self):
    self.commonData.update({
      'cash_available_for_trading': self.dataDict['currentBalances']['cashAvailableForTrading'],
      'cash_available_for_withdrawal': self.dataDict['currentBalances']['cashAvailableForWithdrawal'],
      'cash_call': self.dataDict['currentBalances']['cashCall'],
      'long_non_marginable_market_value': self.dataDict['currentBalances']['longNonMarginableMarketValue'],
      'total_cash': self.dataDict['currentBalances']['totalCash'],
      'cash_debit_call_value': self.dataDict['currentBalances']['cashDebitCallValue'],
      'unsettled_cash': self.dataDict['currentBalances']['unsettledCash']
    })
 
class CashProjectedBalancesParse:
  def __init__(self, dataDict):
    self.dataDict = dataDict
   
   
class MarginInitialBalancesParse(BalanceBase):
  def __init__(self, dataDict):
    super().__init__(dataDict)
    self.dataDict = dataDict
    self.commonData = self._getCommonInitialData()

  def _getData(self):
    self.commonData.update({
      'available_funds_non_marginable_trade': self.dataDict['initialBalances']['availableFundsNonMarginableTrade'],
      'buying_power': self.dataDict['initialBalances']['buyingPower'],
      'day_trading_power': self.dataDict['initialBalances']['dayTradingPower'],
      'day_trading_buying_power_call': self.dataDict['initialBalances']['dayTradingBuyingPowerCall'],
      'day_trading_equity_call': self.dataDict['initialBalances']['dayTradingEquityCall'],
      'equity': self.dataDict['initialBalances']['equity'],
      'equity_percentage': self.dataDict['initialBalances']['equityPercentage'],
      'long_margin_value': self.dataDict['initialBalances']['longMarginValue'],
      'maintenance_call': self.dataDict['initialBalances']['maintenanceCall'],
      'maintenance_requirement': self.dataDict['initialBalances']['maintenanceRequirement'],
      'margin': self.dataDict['initialBalances']['margin'],
      'margin_equity': self.dataDict['initialBalances']['marginEquity'],
      'reg_t_call': self.dataDict['initialBalances']['regTCall'],
      'short_margin_value': self.dataDict['initialBalances']['shortMarginValue'],
      'total_cash': self.dataDict['initialBalances']['totalCash'],
      'margin_balance': self.dataDict['initialBalances']['marginBalance']
    })

class MarginCurrentBalancesParse(BalanceBase):
  def __init__(self, dataDict):
    super().__init__(dataDict)
    self.dataDict = dataDict
    self.commonData = self._getCommonCurrentData()

  def _getData(self):
    self.commonData.update({
      'available_funds': self.dataDict['currentBalances']['availableFunds'],
      'available_funds_non_marginable_trade': self.dataDict['currentBalances']['availableFunds'],
      'buying_power': self.dataDict['currentBalances']['buyingPower'],
      'buying_power_non_marginable_trade': self.dataDict['currentBalances']['buyingPowerNonMarginableTrade'],
      'day_trading_buying_power': self.dataDict['currentBalances']['dayTradingBuyingPower'],
      'equity': self.dataDict['currentBalances']['equity'],
      'equity_percentage': self.dataDict['currentBalances']['equityPercentage'],
      'long_margin_value': self.dataDict['currentBalances']['longMarginValue'],
      'maintenance_call': self.dataDict['currentBalances']['maintenanceCall'],
      'maintenance_requirement': self.dataDict['currentBalances']['maintenanceRequirement'],
      'margin_balance': self.dataDict['currentBalances']['marginBalance'],
      'reg_t_call': self.dataDict['currentBalances']['regTCall'],
      'short_balance': self.dataDict['currentBalances']['shortBalance'],
      'short_margin_value': self.dataDict['currentBalances']['shortMarginValue'],
      'sma': self.dataDict['currentBalances']['sma']
      })
 
class MarginProjectedBalancesParse:
  def __init__(self, dataDict):
    self.dataDict = dataDict
