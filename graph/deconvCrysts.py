import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib as mlt
from graph.params import *

def getNames(pType: str):
	rootPath = "/home/sewik/source/repos/Spectra/data/"
	filesPath = os.path.join(rootPath, pType, 'csvCombined/')
	files = os.listdir(filesPath)
	names = np.array([], dtype='str')
	for file in files:
		if file.__contains__(".CSV"):
			names = np.append(names, file[:-4])
	return names


def getIds(fullList, names, prefix: str):
	ids = np.array([], dtype = 'str')
	for nameToFind in names:
		for index, name in enumerate(fullList):
			if name == nameToFind:
				ids = np.append(ids, f'{prefix}{index + 1}')
	return ids


def plot_deconv_cryst_general(
		path: str,
		files: list[str],
		deconv: str,
		corr: str,
		pType: str,
		lamb: str,
		sec: str,
		num: str,
		outPath: str
):
	# mlt.use("Cairo")

	namesList = getNames(pType = pType)
	prefix = pType[0].upper()
	for file in files:
		content = np.loadtxt(path + file, delimiter=';', dtype = 'str')
		names = content[:, 0]
		values = content[:, 1]
		figure, axis = plt.subplots()
		multiplier = 0
		while True:
			start = multiplier * 10
			end = (multiplier + 1) * 10
			if end > len(names):
				end = len(names) - 1
				if end < start:
					end = start
			multiplier = multiplier + 1
			outFileName = outPath + f'{num}_{pType[0].upper()}{start + 1}-{pType[0].upper()}{end + 1}_{deconv}_{corr}_{lamb}_{sec}.png'
			if os.path.exists(outFileName):
				print(f'Skipping: {outFileName}')
				continue
			X = getIds(fullList=namesList, names=names[start:end], prefix = prefix)
			Y = np.array(values[start:end], dtype='float')
			if start > len(names):
				break
			axis.set_ylabel('Wartość')
			axis.set_xlabel('Nazwa próbki')
			try:
				plt.scatter(X, Y, color = colors[num])
			except ValueError:
				print(X.size)
				print(Y.size)
				print(path+file)
				exit(1)
			plt.legend(num)
			if not os.path.exists(outPath):
				os.makedirs(outPath)
			# plt.show()
			plt.savefig(
				fname = outFileName,
				dpi = 200
			)
			plt.close()
			print(f'Saved: {outFileName}')