#!/usr/bin/env python

import tomopy
import time

# data I/O: http://tomopy.readthedocs.org/en/latest/source/api/tomopy.io.writer.html
# data I/O: http://tomopy.readthedocs.org/en/latest/source/api/tomopy.io.reader.html

'''
bl832 test hdf5 file: center of rotation
'20150820_130628_Dleucopodia_10458_pieceA_10x_z30mm.h5': 1155.75
'20150820_124324_Dleucopodia_10458_pieceA_10x_z80mm_moreangles.h5': 1223,
'20140829_132953_euc60mesh_1M-KI_10percLoad_time0_5x_33p5keV_10cmSampDet.h5': 1334.85
These files can be found in /global/cscratch1/sd/lbluque/tomobench_datasets
'''
fname = "path/to/bl832.h5"


# Load real data from ALS 832 ------------

# load DataExchange data
t = time.time()
prj, flt, drk, flc = tomopy.read_als_832h5(fname) # sino=(1000, 1032)) #sino kwarg only if you only what to read in a subset of sinograms
# ignore the flc variable...
print prj.shape, flt.shape, drk.shape
print time.time() - t

# define projection angles
ang = tomopy.angles(prj.shape[0])

# data normalization
t = time.time()
prj = tomopy.normalize(prj, flt, drk)
print time.time() - t


# Processing funcs --------------

# reconstruct
t = time.time()
rec = tomopy.recon(prj, ang,
	algorithm='gridrec',
	center=, #Add center from above
	emission=False)
print time.time() - t

# -----------------------------


# save as tiff stack
tomopy.write_tiff_stack(rec, overwrite=False)
