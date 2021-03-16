

class Base:

	def __init__(self, dataDict):
		for key, value in dataDict.items():
			setattr(self, key, value)


	def main(self):

		print(self.__dict__)
		print('type: '+self.type)

