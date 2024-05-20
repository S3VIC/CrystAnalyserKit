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
			if start > len(names):
				break
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
			plt.savefig(
				fname = outFileName,
				dpi = 200
			)
			plt.close()
			print(f'Saved: {outFileName}')


def plot_deconv_cryst_lambda_fixed(
		dataDict: dict,
		corr: str,
		pType: str,
		num: str,
		outPath: str
):
	prefix = pType[0].upper()
	fullNamesList = getNames(pType = pType)
	for index, name in enumerate(fullNamesList):
		fileName = outPath + f'{prefix}{index+1}.png'
		if not os.path.exists(outPath):
			os.makedirs(outPath)
		if os.path.exists(fileName):
			print(f"Skipping: {fileName}")
			continue
		fig, ax = plt.subplots()
		X = np.array(list(dataDict.keys()), dtype = 'float')
		Y = np.array([], dtype = 'float')
		for secondValue, data in dataDict.items():
			foundRecord = False
			for probeNumber, probeName in enumerate(data[:, 0]):
				if probeName != name:
					continue
				if data[probeNumber, 1] == '':
					Y = np.append(Y, float(-5))
					foundRecord = True
					break
				Y = np.append(Y, float(data[probeNumber, 1]))
				foundRecord = True
				break
			if not foundRecord:
				Y = np.append(Y, float(-5))
		plt.scatter(X, Y, color = colors[num])
		ax.set_ylabel('Wartość')
		if corr == 'asLS':
			xLabel = 'Współczynnik terminacji'
		else:
			xLabel = 'Waga asymetrii'
		ax.set_xlabel(xLabel)
		maxY = np.max(Y)
		prunedYMask = Y >= 0
		prunedY = Y[prunedYMask]
		if prunedY.size != 0:
			minY = np.min(prunedY)
		else:
			minY = np.min(Y)
		factor = 0.05
		ax.set_ylim((minY - factor * minY, maxY + factor*maxY))
		legendRecord = f'{prefix}{index + 1}'
		plt.legend([legendRecord])
		# plt.show()
		plt.savefig(
			fname = fileName,
			dpi=200
		)
		plt.close()
		print(f"Saved: {fileName}")

def plot_deconv_cryst_second_fixed(
		dataDict: dict,
		pType: str,
		num: str,
		outPath: str
):
	prefix = pType[0].upper()
	fullNamesList = getNames(pType)
	for index, name in enumerate(fullNamesList):
		fileName = outPath + f'{prefix}{index + 1}.png'
		if not os.path.exists(outPath):
			os.makedirs(outPath)
		if os.path.exists(fileName):
			print(f'Skipping: {fileName}')
			continue

		fig, ax = plt.subplots()
		X = np.array(list(dataDict.keys()), dtype = 'float')
		Y = np.array([], dtype = 'float')
		for lambdaValue, data in dataDict.items():
			foundRecord = False
			for probeNumber, probeName in enumerate(data[:, 0]):
				if probeName != name:
					continue
				if data[probeNumber, 1] == '':
					Y = np.append(Y, float(-5))
					foundRecord = True
					break
				Y = np.append(Y, float(data[probeNumber, 1]))
				foundRecord = True
				break
			if not foundRecord:
				Y = np.append(Y, float(-5))
		plt.scatter(X, Y, color = colors[num])
		ax.set_ylabel('Wartość')
		ax.set_xlabel('Parametr wygładzający')
		maxY = np.max(Y)
		prunedYMask = Y >= 0
		prunedY = Y[prunedYMask]
		if prunedY.size != 0:
			minY = np.min(prunedY)
		else:
			minY = np.min(Y)
		factor = 0.05
		ax.set_ylim((minY - factor* minY, maxY + factor * maxY))
		plt.xscale('log')
		legendRecord = f'{prefix}{index + 1}'
		plt.legend([legendRecord])
		#plt.show()
		plt.savefig(
			fname = fileName,
			dpi=200
		)
		plt.close()
		print(f'Saved: {fileName}')
