import logging

log = logging.getLogger(__name__)
class PositionsParse:
    
  def __init__(self, dataDict):
    self.dataDict = dataDict 
    self.positions = self.dataDict['securitiesAccount']['positions']

  def _getData(self):
    parsedPositions = []    
    for position in self.positions:    
      try:
        parsedPosition = {
          'account_id': self.dataDict['securitiesAccount']['accountId'],
          'short_quantity': position['shortQuantity'],
          'average_price': position['averagePrice'],
          'current_day_profit_loss': position['currentDayProfitLoss'],
          'current_day_profit_loss_percentage': position['currentDayProfitLossPercentage'],
          'long_quantity': position['longQuantity'],
          'settled_long_quantity': position['settledLongQuantity'],
          'settled_short_quantity': position['settledShortQuantity'],
          'asset_type': position['instrument']['assetType'],
          'cusip': position['instrument']['cusip'],
          'symbol': position['instrument']['symbol'],
          'market_value': position['marketValue'],
          'maintenance_requirement': position['maintenanceRequirement'],
          'current_day_cost': position['currentDayCost'],
          'previous_session_long_quantity': position['previousSessionLongQuantity'] 
        }

        if parsedPosition['asset_type'] == 'CASH_EQUIVALENT':
          parsedPosition.update({
            'instrument_description': position['instrument']['description'],
            'instrument_type': position['instrument']['type'],
          })
        
        elif parsedPosition['asset_type'] == 'OPTION':
          parsedPosition.update({
            'instrument_description': position['instrument']['description'],
            'put_or_call': position['instrument']['putCall'],
            'underlying_symbol': position['underlyingSymbol']
          })

      except KeyError as e:
        log.exception(f'Logical Error in PositionParse._getData(): \n{e}\n\n API Dict: {self.dataDict}\n') 
      
      else:
        parsedPositions.append(parsedPosition)  

    return parsedPositions

  def main(self):
    return self._getData()