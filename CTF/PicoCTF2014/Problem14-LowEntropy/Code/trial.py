#!/usr/bin/env python
import os
import SocketServer
import threading
import random
import time


with open('keys.txt') as my_file:
    testsite_array = my_file.readlines()

thefile = open('test.txt', 'w')

for line in testsite_array:
	print line;
	thefile.write(str(int(line,16)))
	thefile.write('\n\n')

