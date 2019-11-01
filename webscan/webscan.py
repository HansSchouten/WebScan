import pandas as pd
from pyquery import PyQuery as pq

from webscan.scanners import *

class WebScan:
	"""
	This class can scan websites with various defined scanners.

	"""

	def __init__(self):
		self.scanners = [
			Laravel()
		]

		self.domains = pd.read_csv('data/domains.csv')

	def start(self):
		"""
		Start scanning the configured list of domains.

		"""
		for index, row in self.domains.iterrows():
			self.scan(row.domain)

	def scan(self, domain):
		"""
		Scan the given domain with all configured scanners.

		"""
		for scanner in self.scanners:
			path = scanner.getPath()
			url = domain + path
			response = self.performRequest(url)
			if (response and scanner.hasMatch(response)):
				self.processMatch(url, response.html())

	def processMatch(self, url, data):
		"""
		Log that a successful scan result was obtained.

		"""
		print("Match found on " + url)

	def performRequest(self, url):
		"""
		Perform an HTTP GET request to the given URL and return the response.

		"""
		try:
			return pq(url=url)
		except:
			return None