#!/usr/bin/env python

import tomopy
import numpy
import time

print "Hey!"

obj = numpy.ones((512, 512, 512), dtype='float32')
ang = tomopy.angles(512)

t = time.time()
prj = tomopy.project(obj, ang)
print time.time() - t

t = time.time()
rec = tomopy.recon(prj, ang, algorithm='gridrec', num_gridx=1024, num_gridy=1024)
print time.time() - t

tomopy.write_tiff_stack(rec, overwrite=True)
