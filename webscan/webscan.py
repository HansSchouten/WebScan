import pandas as pd
from datetime import datetime
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

		self.logFile = open('data/results.txt','a')
		self.domains = pd.read_csv('data/domains.csv')

	def start(self):
		"""
		Start scanning the configured list of domains.

		"""
		l = self.domains.shape[0]
		self.printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

		for index, row in self.domains.iterrows():
			self.scan(row.domain)
			self.printProgressBar(index + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

	def scan(self, domain):
		"""
		Scan the given domain with all configured scanners.

		"""
		for scanner in self.scanners:
			path = scanner.getPath()
			url = "https://" + domain + "/" + path
			response = self.performRequest(url)
			if (response and scanner.hasMatch(response)):
				self.processMatch(url, response.html())

	def processMatch(self, url, data):
		"""
		Log that a successful scan result was obtained.

		"""
		message = "Match found on " + url
		self.logFile.write(str(datetime.now()) + "\n")
		self.logFile.write(message + "\n\n")

	def performRequest(self, url):
		"""
		Perform an HTTP GET request to the given URL and return the response.

		"""
		try:
			return pq(url=url)
		except:
			return None

	def printProgressBar(self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
		"""
		Call in a loop to create terminal progress bar
		@params:
			iteration   - Required  : current iteration (Int)
			total       - Required  : total iterations (Int)
			prefix      - Optional  : prefix string (Str)
			suffix      - Optional  : suffix string (Str)
			decimals    - Optional  : positive number of decimals in percent complete (Int)
			length      - Optional  : character length of bar (Int)
			fill        - Optional  : bar fill character (Str)
			printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
		"""
		percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
		filledLength = int(length * iteration // total)
		bar = fill * filledLength + '-' * (length - filledLength)
		print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
		# Print New Line on Complete
		if iteration == total: 
			print()