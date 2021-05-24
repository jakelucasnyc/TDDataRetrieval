import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from secrets import dbSecrets
import logging

log = logging.getLogger(__name__)
class DBConnection:

	def __init__(self):
		self.db = None
		config = {
			'user': dbSecrets.USER,
			'password': dbSecrets.PASS,
			'host': '127.0.0.1',
			'database': 'td_ameritrade_data',
			# 'raise_on_warnings': True
		}

		try:
			self.db = mysql.connector.connect(**config)

		except Error as e:
			if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				log.error('DB Server Username or Password is Invalid')
			elif e.errno == errorcode.ER_BAD_DB_ERROR:
				log.error("DB Doesn't exist")

			else:
				log.error(e)
		else:
			log.info('Successfully Connected to Database')

	def __del__(self):
		if self.db is not None:
			self.db.close()



	def insertTransaction(self, parsedData: dict):
		if self.db is None:
			log.warning('Not connected to database. Insertion aborted')
			return
		if not parsedData:
			log.warning('No data in parsed dictionary. Insertion aborted')
			return
		#creating a list of the keys to use in inserting data into the sql table
		
		keysString = ", ".join(list(parsedData.keys())[1:])
		# insertData = ", ".join(valuesList)
		log.debug(parsedData.keys())
		log.debug(parsedData.values())

		#creating the same number of "%s" symbols as there are keys in the parsedData. This makes this function flexible for different types of transactions
		
		strFormatString = ", ".join(['%s'] * len(list(parsedData.keys())[1:]))

		#formatting the INSERT statement 
		addData = (
			f'REPLACE INTO {parsedData["table"]} '
			f'({keysString}) '
			f'VALUES ({strFormatString})'
			)


		#inserting and committing to the database
		with self.db.cursor() as cursor:
			cursor.execute(addData, list(parsedData.values())[1:])
			self.db.commit()





