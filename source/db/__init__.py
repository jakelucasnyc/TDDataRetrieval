
from appSecrets import dbSecrets
import sys
import logging
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.dialects.mysql import insert
from db.base import tableBase
from db.transactions import *

log = logging.getLogger(__name__)
class DBConnection:

    DATABASE_URL = f'mysql+pymysql://{dbSecrets.USER}:{dbSecrets.PASS}@{dbSecrets.HOST}:{dbSecrets.PORT}/td_ameritrade_data'

    def __init__(self):
        self._engine = create_engine(DBConnection.DATABASE_URL, echo_pool=True)
        try:
            testConn = self._engine.connect()
            testConn.close()
        except sqlalchemy.exc.OperationalError as e:
            log.exception('Unable to connect to database. Ending Program')
            sys.exit()
            
        self._session = sessionmaker(self._engine)
        tableBase.metadata.create_all(self._engine)
        self.tableModels = {cls.__tablename__: cls for cls in tableBase.__subclasses__()}



    def insert(self, parsedData: dict):

      if parsedData == {}:
        log.error('No data to insert. Insertion aborting...')
        return
      with self._session() as conn:
        with conn.begin():
          try: 

            if parsedData['table'] not in self.tableModels.keys():
              log.warning("Destination table not found. Insertion Aborted")    
          except Exception as e:
              log.error('No table in parsed dictionary')
              log.exception(e)

          tableObj = self.tableModels[parsedData['table']]      
          insertedData = {key: value for key, value in parsedData.items() if key != 'table'}
          log.debug(f'Inserted Data: {insertedData}')
          ins = insert(tableObj).values(**insertedData)
          #if a duplicate primary key is present, update data without re-inserting primary key
          stmt = ins.on_duplicate_key_update(**{key: value for key, value in insertedData.items() if getattr(tableObj, key).primary_key == True})
          # stmt = ins.on_conflict_do_update(**{key: value for key, value in insertedData.items() if getattr(tableObj, key).primary_key == True})
          conn.execute(stmt)
          conn.commit()


          

