#!/usr/bin/env python
import os
import SocketServer
import threading
import random
import time
from fractions import gcd

with open('test.txt') as my_file:
    testsite_array = my_file.readlines()

thefile = open('factors.txt', 'w')

for i in range (0,1000):
		n1 = 136259180061403755645780975004266422233598506544192215931801748131609480302534477443760975468544253449968417076681136928952693088297386681204178514909429934651184845917372508672772853148336421947772685945971082259065822716273918205644497062070687040688482425772494806977243091877815693515561645032206416314719;
		n2 = (int)(testsite_array[i]);
		thefile.write(str(gcd(n1,n2)));
		thefile.write("\n");

