import unittest

class TestTHParse(unittest.TestCase):

	def test_invalid_type(self):
		"""
		Test that it outputs an empty dict if the type of transaction is invalid
		"""
		dataDict = {
			'type': 'gibberish'
		}
		target = __import__('')
		THParse = target.TransactionHistoryParse(dataDict)

		result = THParse.main()

		self.assertEqual(result, {})


if __name__ == "__main__":
	unittest.main()