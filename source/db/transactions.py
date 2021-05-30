from sqlalchemy import sql
from sqlalchemy.sql.expression import null
from db.base import tableBase
import sqlalchemy
from sqlalchemy.dialects.mysql import INTEGER

class TradeTransactions(tableBase):
    
    __tablename__ = 'trade_transactions'

    type = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    transaction_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    settlement_date = sqlalchemy.Column(sqlalchemy.Date)
    transaction_id = sqlalchemy.Column(sqlalchemy.String(20), nullable=False, primary_key=True)
    account_id = sqlalchemy.Column(sqlalchemy.String(20), nullable=False)
    expiration_date = sqlalchemy.Column(sqlalchemy.DateTime)
    ticker = sqlalchemy.Column(sqlalchemy.String(7))
    symbol = sqlalchemy.Column(sqlalchemy.String(30))
    cusip = sqlalchemy.Column(sqlalchemy.String(30))
    quantity_shares = sqlalchemy.Column(INTEGER(unsigned=False))
    quantity_contracts = sqlalchemy.Column(INTEGER(unsigned=False))
    cost = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    total_fees = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    fees_dict = sqlalchemy.Column(sqlalchemy.Text)
    put_or_call = sqlalchemy.Column(sqlalchemy.String(10))
    net_amount = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    price_per_share = sqlalchemy.Column(sqlalchemy.Float)
    instrument_description = sqlalchemy.Column(sqlalchemy.Text)
    instruction = sqlalchemy.Column(sqlalchemy.String(15))
    asset_type = sqlalchemy.Column(sqlalchemy.String(15))
    transaction_subtype = sqlalchemy.Column(sqlalchemy.String(10))
    description = sqlalchemy.Column(sqlalchemy.Text)

class ReceiveAndDeliverTransactions(tableBase):
    
    __tablename__ = 'receive_and_deliver_transactions'

    type = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    transaction_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    settlement_date = sqlalchemy.Column(sqlalchemy.Date)
    transaction_id = sqlalchemy.Column(sqlalchemy.String(20), nullable=False, primary_key=True)
    account_id = sqlalchemy.Column(sqlalchemy.String(20), nullable=False)
    net_amount = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    total_fees = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    fees_dict = sqlalchemy.Column(sqlalchemy.Text)
    cost = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    transaction_subtype = sqlalchemy.Column(sqlalchemy.String(10))
    description = sqlalchemy.Column(sqlalchemy.Text)
    quantity_contracts = sqlalchemy.Column(INTEGER(unsigned=False))
    expiration_date = sqlalchemy.Column(sqlalchemy.DateTime)
    cusip = sqlalchemy.Column(sqlalchemy.String(30))
    asset_type = sqlalchemy.Column(sqlalchemy.String(15))
    symbol = sqlalchemy.Column(sqlalchemy.String(30))
    instrument_type = sqlalchemy.Column(sqlalchemy.String(30))

class DividendOrInterestTransactions(tableBase):
    
    __tablename__ = 'dividend_or_interest_transactions'

    type = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    settlement_date = sqlalchemy.Column(sqlalchemy.Date)
    transaction_id = sqlalchemy.Column(sqlalchemy.String(20), nullable=False, primary_key=True)
    account_id = sqlalchemy.Column(sqlalchemy.String(20), nullable=False)
    net_amount = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    transaction_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    total_fees = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    fees_dict = sqlalchemy.Column(sqlalchemy.Text)
    cost = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    transaction_subtype = sqlalchemy.Column(sqlalchemy.String(10))
    description = sqlalchemy.Column(sqlalchemy.Text)

class JournalTransactions(tableBase):
    
    __tablename__ = 'journal_transactions'
    
    type = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    settlement_date = sqlalchemy.Column(sqlalchemy.Date)
    transaction_id = sqlalchemy.Column(sqlalchemy.String(20), nullable=False, primary_key=True)
    account_id = sqlalchemy.Column(sqlalchemy.String(20), nullable=False)
    net_amount = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    transaction_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    total_fees = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    fees_dict = sqlalchemy.Column(sqlalchemy.Text)
    cost = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    transaction_subtype = sqlalchemy.Column(sqlalchemy.String(10))
    description = sqlalchemy.Column(sqlalchemy.Text)
    clearing_reference_number = sqlalchemy.Column(sqlalchemy.String(15))
    ach_status = sqlalchemy.Column(sqlalchemy.String(20))

class ElectronicFundTransactions(tableBase):

    __tablename__ = 'electronic_fund_transactions'

    type = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    settlement_date = sqlalchemy.Column(sqlalchemy.Date)
    transaction_id = sqlalchemy.Column(sqlalchemy.String(20), nullable=False, primary_key=True)
    account_id = sqlalchemy.Column(sqlalchemy.String(20), nullable=False)
    net_amount = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    transaction_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    total_fees = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    fees_dict = sqlalchemy.Column(sqlalchemy.Text)
    cost = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    transaction_subtype = sqlalchemy.Column(sqlalchemy.String(10))
    description = sqlalchemy.Column(sqlalchemy.Text)