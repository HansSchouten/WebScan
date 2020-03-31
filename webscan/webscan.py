import pandas as pd
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from webscan.scanners import *

class WebScan:
	"""
	This class can scan websites with various defined scanners.

	"""

	def __init__(self):
		self.scanners = [
			Laravel()
		]

		self.domains = pd.read_csv('data/top-1m.csv').iloc[::-1]

	def start(self):
		"""
		Start scanning the configured list of domains.

		"""
		self.total = self.domains.shape[0]
		self.index = 0

		
		processes = []
		with ThreadPoolExecutor(max_workers=10) as executor:
			for index, row in self.domains.iterrows():
				processes.append(executor.submit(self.scan, row.domain))

	def scan(self, domain):
		"""
		Scan the given domain with all configured scanners.

		"""
		for scanner in self.scanners:
			path = scanner.getPath()
			url = "https://" + domain + "/" + path
			response = self.performRequest(url)
			if (response and scanner.hasMatch(response.text)):
				self.processMatch(url, response.text)

		# print progress
		self.index = self.index + 1
		self.printProgressBar(self.index, self.total, prefix = 'Progress:', suffix = 'Complete', length = 50)

	def processMatch(self, url, data):
		"""
		Log that a successful scan result was obtained.

		"""
		message = "Match found on " + url
		self.log("\n" + str(datetime.now()) + "\n" + message + "\n\n")

	def performRequest(self, url):
		"""
		Perform an HTTP GET request to the given URL and return the response.

		"""
		self.log("Requesting: " + url + "\n")
		try:
			return requests.get(url=url, timeout=2)
		except:
			return None
		
	def log(self, message):
		"""
		Log the given message.

		"""
		logFile = open('data/results.txt','a')
		logFile.write(message)
		logFile.close()

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