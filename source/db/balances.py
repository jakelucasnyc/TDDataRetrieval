from db.base import tableBase
import sqlalchemy

class InitialBalances(tableBase):
  
  __tablename__ = 'initial_balances'
  
class CurrentBalances(tableBase):
  
  __tablename__ = 'current_balances'
  
class ProjectedBalances(tableBase):
  
  __tablename__ = 'projected_balances'