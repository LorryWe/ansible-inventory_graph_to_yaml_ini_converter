#!/usr/bin/python
#
# Script to reformat ansible-inventory <foreman> --graph output
# ...to a usable yaml or ini inventory file
#
# 20200421	L Weston
#
#########################################################

import sys, getopt, re

def main(argv):
	# Vars
	groupnamematch = "^.*\|\-\-\@"
	managednodematch = "^.*\|  \|\-\-"
	headermatch = "^\@all\:"
	ungroupedmatch = groupnamematch+"ungrouped\:"
	inputfile = ""
	outputfile = ""
	foremanservername = ""
	usage = 'Usage: convert_graph_inventory.py -i <output from ansible-inventory --graph> [-f <foremanservername>] [-o <outputfile>]'
	
	# Check args
	if len(sys.argv) <2:
		print usage
		exit(1)
	try:
		opts, args = getopt.getopt(argv,"h:i:o:f:",["ifile=","ofile=","foremanserver"])
	except getopt.GetoptError:
		print usage
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print usage 
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-f", "--foremanserver"):
			foremanservername = arg

	# Load inputfile into listin
        try:
                listin = list(open(inputfile))
        except IOError:
                print("Something is wrong with inputfile ",inputfile)

	# Process listin
	for line in listin:
        	# Tidy up end of all lines
        	if line.endswith ('\n'):
        	        line = line[:-1]

        	# Process header
		header = re.match(headermatch,line)
		if header:
			line = re.sub(headermatch,"",line)
        		line = re.sub(r"(.*)","---",line)
			print(line)

        	# Process groupname
        	groupname = re.match(groupnamematch,line)
        	if groupname:
			ungrouped = re.match(ungroupedmatch,line)
			if ungrouped:
				line = re.sub(ungroupedmatch,"",line)
				line = re.sub(r"(.*)","foreman_ungrouped:",line)
			line = re.sub(groupnamematch,"",line)
			line = re.sub(r"(.*)","  \g<1>",line)
			line = re.sub("foreman_",foremanservername+"_",line)
        	        print(line)
        	        print("    hosts:")

        	# Process managednode name
        	managednode = re.match(managednodematch,line)
        	if managednode:
			line = re.sub(managednodematch,"",line)
        	        line = re.sub(r"(.*)","      \g<1>:",line)
        	        print(line)

if __name__ == "__main__":
	main(sys.argv[1:])
