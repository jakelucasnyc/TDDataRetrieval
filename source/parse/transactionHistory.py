from Parse.Base import Base

class TransactionHistoryParse(Base):

	def __init__(self, dataDict):
		super().__init__(dataDict)

	def main(self):
		print(self.__dict__)