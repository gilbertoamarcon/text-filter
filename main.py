#!/usr/bin/env python


import argparse
import re

PROB = '((?:problem \d+)|(?:problems \d+ and \d+)|(?:problems (?:\d+, )+and \d+))'
AUTOREF = '(as (?:presented|shown) in .*)'
GENERAL = '(.*)'
FMAX = '(\$f_\{max\} = \d\.\d{2}\$)'
INT = '(\d+)'


MIX = {
	'prob-failed': {
		'keys': (GENERAL,PROB,AUTOREF),
		'templates': [
			r'%s failed to generate valid plans for %s, %s',
			r'%s generated no valid plans for %s, %s',
			r'%s did not generate valid plans for %s, %s',
			r'No valid plans were generated by %s for %s, %s',
		],
	},
	'prob-succeeded': {
		'keys': (GENERAL,PROB,AUTOREF),
		'templates': [
			r'%s solved %s for all coalitions, %s',
			r'%s generated valid plans for %s for all coalitions, %s',
			r'Valid plans were generated by %s for %s, %s',
		],
	},
	'prob-both': {
		'keys': (GENERAL,PROB,PROB,AUTOREF),
		'templates': [
			r'%s did not generate valid plans for %s and solved %s for all coalitions, %s',
			r'%s failed to generate valid plans for %s and generated valid plans for %s for all coalitions, %s',
			r'%s generated no valid plans for %s and solved %s for all coalitions, %s',
			r'%s did not generate valid plans for %s and generated valid plans for %s for all coalitions, %s',
			r'%s failed to generate valid plans for %s and solved %s for all coalitions, %s',
			r'%s generated no valid plans for %s and generated valid plans for %s for all coalitions, %s',
		],
	},
	'succ-count-fail': {
		'keys': (FMAX,INT,INT,AUTOREF),
		'templates': [
			r'All %s heuristics failed to produce a valid plan for %s out of the 100 problems, i.e., at least one heuristic succeeded in producing a valid plan for %s out of the 100 problems, %s',
			r'All %s heuristics failed to generate a valid plan for %s out of the 100 problems, i.e., at least one heuristic succeeded in producing a valid plan for %s out of the 100 problems, %s',
			r'All %s heuristics failed to produce a valid plan for %s out of the 100 problems, i.e., at least one heuristic succeeded in generating a valid plan for %s out of the 100 problems, %s',
			r'All %s heuristics failed to generate a valid plan for %s out of the 100 problems, i.e., at least one heuristic succeeded in generating a valid plan for %s out of the 100 problems, %s',
		],
	},
	'succ-count-succ': {
		'keys': (FMAX,INT,INT,AUTOREF),
		'templates': [
			r'All %s heuristics succeeded in generating a valid plan for %s out of the 100 problems, i.e., at least one heuristic failed to produce a valid plan for %s out of the 100 problems, %s',
			r'All %s heuristics succeeded in producing a valid plan for %s out of the 100 problems, i.e., at least one heuristic failed to produce a valid plan for %s out of the 100 problems, %s',
			r'All %s heuristics succeeded in generating a valid plan for %s out of the 100 problems, i.e., at least one heuristic failed to generate a valid plan for %s out of the 100 problems, %s',
			r'All %s heuristics succeeded in producing a valid plan for %s out of the 100 problems, i.e., at least one heuristic failed to generate a valid plan for %s out of the 100 problems, %s',
		],
	},
}





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

def mix(data,base=False):
	if not base:
		data = mix(data,base=True)
	for mode in MIX.values():
		# for t in mode['templates']:
		# 	print t%mode['keys']
		for i,m in enumerate([{'template':t,'matches':m} for t in mode['templates'] for m in re.findall((t%mode['keys']),data)]):
			original = m['template']%m['matches']
			new = mode['templates'][0 if base else i%len(mode['templates'])]%m['matches']
			new = new.replace(' The',' the')
			data = data.replace(original,new)
	return data

def filter(filename):
	print 'File %s:'%filename

	with open(filename,'r') as f:
		data = f.read()
		acro_ref(data)
		serial_comma(data)
		data = mix(data)

	with open(filename,'w') as f:
		f.write(data)

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
