#!/usr/bin/env python

with open('keys.txt') as my_file:
    testsite_array = my_file.readlines()

thefile = open('test.txt', 'w')

for line in testsite_array:
	print line;
	thefile.write(str(int(line,16)))
	thefile.write('\n\n')

