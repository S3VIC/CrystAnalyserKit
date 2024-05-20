import os.path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlt
from graph.params import *
from crystanalyser.analyser import *


def prepare_ids(names, prefix, indexStart, indexEnd):
	for i in range(indexStart, indexEnd):
		names[i - indexStart] = str(prefix[0]) + str(i)
	return names


def plot_raw(names, values, prefix, correctMethod, crystNum, lambdaValue, secondParam, pathToSave):
	mlt.use("Cairo")
	figure, axis = plt.subplots()
	multiplier = 0
	while(True):
		start = multiplier * 10
		end = (multiplier + 1) * 10 - 1
		if end > len(names):
			end = len(names) - 1
			if end < start:
				end = start
		X = prepare_ids(names[start:end], prefix, start, end)
		Y = np.array(values[start:end], dtype='float')
		if start > len(names):
			break
		multiplier = multiplier + 1
		axis.set_ylabel('Wartość')
		axis.set_xlabel('Nazwa próbki')
		plt.scatter(X, Y, color = colors[crystNum])
		plt.legend(crystNum)
		if not os.path.exists(pathToSave):
			os.makedirs(pathToSave)
		fileName = pathToSave + f'{crystNum}_{prefix}{start}-{prefix}{end}_{correctMethod}_{lambdaValue}_{secondParam}.png'
		plt.savefig(
			fname = fileName,
			dpi=200
		)
		plt.close()
		print(f'Saved: {fileName}')


def plot_raw_lambda_fixed(contentDict, prefix, probeNames, bgCorrection: str, crystNumber, pathToSave):
	mlt.use("Cairo")
	for index, probeName in enumerate(probeNames):
		figure, axis = plt.subplots()
		X = np.array([], dtype = 'float')
		Y = np.array([], dtype = 'float')
		for secondParam, content in contentDict.items():
			name = content[index, 0]
			X = np.append(X, float(secondParam))
			if content[index, 1] == '':
				Y = np.append(Y, float(-5))
			else:
				Y = np.append(Y, float(content[index, 1]))
			if not name.__contains__(probeName):
				print(False)
			plt.scatter(X, Y, color = colors[crystNumber])
		legend = f'{prefix}{index}'
		plt.legend([legend])
		if bgCorrection == 'asLS':
			xLabel = 'Współczynnik terminacji'
		else:
			xLabel = 'Waga asymetrii'
		axis.set_ylabel('Wartość')
		axis.set_xlabel(xLabel)
		if not os.path.exists(pathToSave):
			os.makedirs(pathToSave)
		fileName = pathToSave + f'{prefix}{index}-{crystNumber}-{bgCorrection}.png'
		plt.savefig(
			fname = fileName,
			dpi=200
		)
		plt.close()
		print(f'Saved: {fileName}')


def plot_raw_second_fixed(contentDict, probeNames, correctionMethod, prefix, path):
	for index, name in enumerate(probeNames):
		if correctionMethod == 'asLS':
			secondValues = secondAsLSList
		else:
			secondValues = secondArLSList
		for secondValue in secondValues:
			xDict = {
				'1': np.array([], dtype='float'),
				'2': np.array([], dtype='float'),
				'3': np.array([], dtype='float'),
				'4': np.array([], dtype='float')
			}
			yDict = {
				'1': np.array([], dtype='float'),
				'2': np.array([], dtype='float'),
				'3': np.array([], dtype='float'),
				'4': np.array([], dtype='float')
			}
			for lambdaValue, crystData in contentDict.items():
				for crystNum, fileNames in crystData.items():
					for record in fileNames:
						if record.split('-')[3] == str(secondValue):
							content = np.loadtxt(record, delimiter="$", dtype='str')
							for number, probeName in enumerate(content[:, 0]):
								if probeName == name:
									xDict[crystNum] = np.append(xDict[crystNum], float(lambdaValue))
									if content[number, 1] != '':
										yDict[crystNum] = np.append(yDict[crystNum], float(content[number, 1]))
									else:
										yDict[crystNum] = np.append(yDict[crystNum], float(0))
									break
								else:
									continue

			for crystNum in xDict.keys():
				figure, axis = plt.subplots()
				plt.scatter(xDict[crystNum], yDict[crystNum], color = colors[crystNum])
				plt.xscale('log')
				legend = f'{prefix}{index}'
				plt.legend([legend])
				axis.set_ylabel('Wartość')
				axis.set_xlabel('Parametr wygładzający')
				pathToSave = os.path.join(path, str(secondValue), correctionMethod + '/')
				imageName = pathToSave + f'{prefix}{index}-{crystNum}-{correctionMethod}-{secondValue}.png'
				if not os.path.exists(pathToSave):
					os.makedirs(pathToSave)
				if os.path.exists(imageName):
					print(f"Already exists: {imageName}")
					continue
				plt.savefig(imageName, dpi=200)
				print(f'Saved: {imageName}')
				plt.close()
