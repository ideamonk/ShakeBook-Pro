#!/usr/bin/env python

import applesms
import time

try:
	while(True):
		(x, y, z) = applesms.coords()
		print (x, y, z)
		time.sleep(1)
except applesms.error, e:
	print 'an error occurred: %s' % str(e)

