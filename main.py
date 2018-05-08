#!/usr/bin/env python


import argparse
import re

def acro_ref(data):
	pattern = r'((?:(?!and)(?!The)(?!the)(?:\b\w+\b)[-\s]*)+)\s+\((\w+)\s+[\d\.]+\)'
	print 'acro_ref:'
	for r in set(re.findall(pattern, data)):
		if ''.join([w[0] for w in re.findall(r'(\w+)', r[0])]) != r[1]:
			print '\t'+r

def serial_comma(data):
	pattern = r'((?:[^,\s]+, +)+[^,\s]+ +and +[^,\s])'
	print 'serial_comma:'
	for r in set(re.findall(pattern, data)):
		print '\t'+r

def filter(filename):
	print 'File %s:'%filename
	with open(filename,'r') as f:
		data = f.read()
		acro_ref(data)
		serial_comma(data)

def main():

	# Parsing user input
	parser = argparse.ArgumentParser()
	parser.add_argument(
			'-i','--inputs',
			nargs='*',
			required=True,
			help='Input file names.'
		)
	args = parser.parse_args()

	for f in args.inputs:
		filter(filename=f)






if __name__ == "__main__":
	main()
