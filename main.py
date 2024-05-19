#!/usr/bin/python3
from dataextract.raw import *
from dataextract.deconv import *

if __name__ == "__main__":
	rootDataDir = "/home/sewik/source/repos/CrystAnalyserKit/data/deconvCrysts"
	# raw_cryst_general()
	# raw_cryst_lambda_fixed()
	# raw_cryst_second_fixed()
	deconv_crysts_general(path = rootDataDir)

