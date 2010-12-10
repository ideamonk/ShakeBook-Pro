#!/usr/bin/env python

'''
  ShakeBook Pro - tilt your mbp to switch desktop.
    // I use option+arrow to switch, 
        modify the applescripts to suit yours //

                                -- Abhishek Mishra < ideamonk@gmail.com >

'''


import applesms
import time
import os

threshold = 20;

try:
    while(True):
        (x, y, z) = applesms.coords()
        if x>threshold:
            os.system("./left.applescript")
            time.sleep(1)
        if x<-threshold:
            os.system("./right.applescript")
            time.sleep(1)
        time.sleep(0.02)
except applesms.error, e:
    print 'an error occurred: %s' % str(e)

