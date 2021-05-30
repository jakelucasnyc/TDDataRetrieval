

class Base:

	def __init__(self, dataDict):
		self.dataDict = dataDict
		for key, value in dataDict.items():
			setattr(self, key, value)



