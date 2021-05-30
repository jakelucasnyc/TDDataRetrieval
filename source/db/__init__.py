
from secrets import dbSecrets
import logging
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import insert
from db.base import tableBase
from db.transactions import *

log = logging.getLogger(__name__)
class DBConnection:

    DATABASE_URL = f'mysql+pymysql://{dbSecrets.USER}:{dbSecrets.PASS}@{dbSecrets.HOST}/td_ameritrade_data?charset=utf8mb4'

    def __init__(self):
        self._engine = create_engine(DBConnection.DATABASE_URL, echo_pool=True)
        self._session = sessionmaker(self._engine)
        self.tableModels = {cls.__tablename__: cls for cls in tableBase.__subclasses__()}



    def insertTransaction(self, parsedData: dict):
      with self._session() as conn:
        with conn.begin():
           
          if parsedData['table'] not in self.tableModels.keys():
            log.warning("Destination table not found. Insertion Aborted")    

          tableObj = self.tableModels[parsedData['table']]      
          insertedData = {key: value for key, value in parsedData.items() if key != 'table'}
          print('Inserted Data: ', insertedData)
          ins = insert(tableObj).values(**insertedData)
          #if a duplicate primary key is present, update data without re-inserting primary key
          stmt = ins.on_duplicate_key_update(**{key: value for key, value in insertedData.items() if getattr(tableObj, key).primary_key == True})
          conn.execute(stmt)
          conn.commit()


          

