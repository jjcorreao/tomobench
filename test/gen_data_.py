#!/usr/bin/env python

import tomopy
import numpy
import time
import logging
import sys
import os

# data I/O: http://tomopy.readthedocs.org/en/latest/source/api/tomopy.io.writer.html
# data I/O: http://tomopy.readthedocs.org/en/latest/source/api/tomopy.io.reader.html
#bbpath=os.getenv('DW_JOB_STRIPED')
bbpath=os.getenv('DW_JOB_STRIPED')

#fname = "/global/cscratch1/sd/alsdata/bbeup/data/Hornby_SLS_2011.h5"
fname = os.path.join(bbpath, 'data/Hornby_SLS_2011.h5')

# Load real data from APS ------------

# load DataExchange data
t = time.time()
prj, flt, drk = tomopy.read_aps_2bm(fname, sino=(1000, 1032))
#print prj.shape, flt.shape, drk.shape
#print time.time() - t
logging.info("prj.shape: %s, flt.shape: %s, drk.shape: %s" % (prj.shape, flt.shape, drk.shape))
logging.info("Read - dt: %s" % (time.time() - t))

# define projection angles
ang = tomopy.angles(prj.shape[0])

# data normalization
t = time.time()
prj = tomopy.normalize(prj, flt, drk)
#print time.time() - t
logging.info("Normalization - dt: %s" % (time.time() - t))

# --------------------------------



# Generate a random matrix with dimensions [dim1, dim2, dim3] -----------

#dim1 = between 1000 and 10000
#dim2 = between 1000 and 10000
#dim3 = between 1000 and 10000
dim1 = 1000

prj = numpy.random.random([dim1,dim1,dim1])

# -----------------------------




# Processing funcs --------------

# phase retrieval
t = time.time()
prj = tomopy.retrieve_phase(prj)
#print time.time() - t
logging.info("Phase - dt: %s" % (time.time() - t))

# reconstruct
t = time.time()
rec = tomopy.recon(prj, ang,
	algorithm='gridrec',
	center=1010,
	alpha=1e-4,
	emission=False)
#print time.time() - t
logging.info("Reconstruction - dt: %s" % (time.time() - t))

# -----------------------------

# save as tiff stack
tomopy.write_tiff_stack(rec, overwrite=False)

