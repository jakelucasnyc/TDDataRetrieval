from db.base import tableBase

class Accounts(tableBase):
    
    __tablename__ = 'accounts'

    account_id = sqlalchemy.Column(sqlalchemy.String(20), nullable=False, primary_key=True)
  
