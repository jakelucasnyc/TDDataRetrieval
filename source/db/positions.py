from db.base import tableBase
import sqlalchemy

class Positions(tableBase):
    
    __tablename__ = 'positions'
    
    position_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    account_id = sqlalchemy.Column(sqlalchemy.String(20), nullable=False)
    short_quantity = sqlalchemy.Column(sqlalchemy.Float)
    average_price = sqlalchemy.Column(sqlalchemy.Float)
    current_day_profit_loss = sqlalchemy.Column(sqlalchemy.Float)
    current_day_profit_loss_percentage = sqlalchemy.Column(sqlalchemy.Float)
    long_quantity = sqlalchemy.Column(sqlalchemy.Float)
    settled_long_quantity = sqlalchemy.Column(sqlalchemy.Float)
    settled_short_quantity = sqlalchemy.Column(sqlalchemy.Float)
    asset_type = sqlalchemy.Column(sqlalchemy.String(15))
    cusip = sqlalchemy.Column(sqlalchemy.String(30))
    symbol = sqlalchemy.Column(sqlalchemy.String(30))
    instrument_description = sqlalchemy.Column(sqlalchemy.Text)
    instrument_type = sqlalchemy.Column(sqlalchemy.String(30))
    market_value = sqlalchemy.Column(sqlalchemy.Float)
    maintenance_requirement = sqlalchemy.Column(sqlalchemy.Float)
    current_day_cost = sqlalchemy.Column(sqlalchemy.Float)
    previous_session_long_quantity = sqlalchemy.Column(sqlalchemy.Float)

    