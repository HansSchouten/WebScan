import sys, getopt, os

from webscan.webscan import WebScan

def main(argv):
	"""
	WebScan entry point.

	"""
	scan = WebScan()
	scan.start()
	

if __name__ == "__main__":
	main(sys.argv[1:])