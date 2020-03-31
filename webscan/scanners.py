from abc import ABC, abstractmethod

class Scanner(ABC):
	"""
	This abstract class defines the structure of a Scanner.

	"""

	@abstractmethod
	def getPath(self):
		"""
		Return the relative path this scanner needs to request

		"""
		return ""

	@abstractmethod
	def hasMatch(self, response):
		"""
		Return whether the scan was successful based on the given response

		"""
		return False


class Laravel(Scanner):
	"""
	This class scans for Laravel misconfigurations.

	"""

	def getPath(self):
		"""
		Return the relative path this scanner needs to request

		"""
		return ".env"

	def hasMatch(self, response):
		"""
		Return whether the scan was successful based on the given response

		"""
		return "APP_ENV=" in response


class Git(Scanner):
	"""
	This class scans for a publicly accessible github repository.

	"""

	def getPath(self):
		"""
		Return the relative path this scanner needs to request

		"""
		return ".git/HEAD"

	def hasMatch(self, response):
		"""
		Return whether the scan was successful based on the given response

		"""
		return "ref:" in response