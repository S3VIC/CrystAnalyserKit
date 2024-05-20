import numpy as np

from graph.deconvCrysts import *

outputRootGeneralPath = "/home/sewik/source/repos/CrystAnalyserKit/images/deconvGeneral"
outputRootLambdaFixed = "/home/sewik/source/repos/CrystAnalyserKit/images/deconvLambdaFixed"

def deconv_crysts_general(path: str):
	deconvMethods = os.listdir(path)
	for method in deconvMethods:
		methodPath = os.path.join(path, method)
		probeTypes = os.listdir(methodPath)
		for probeType in probeTypes:
			probeTypePath = os.path.join(methodPath, probeType)
			correctionTypes = os.listdir(probeTypePath)
			for correction in correctionTypes:
				correctionPath = os.path.join(probeTypePath, correction)
				lambdaValues = os.listdir(correctionPath)
				for lambdaValue in lambdaValues:
					lambdaPath = os.path.join(correctionPath, lambdaValue)
					secondParamValues = os.listdir(lambdaPath)
					for secondValue in secondParamValues:
						secondValuePath = os.path.join(lambdaPath, secondValue)
						crystNumbers = os.listdir(secondValuePath)
						for number in crystNumbers:
							crystPath = os.path.join(secondValuePath, number + '/')
							crystFiles = os.listdir(crystPath)
							outPath = os.path.join(outputRootGeneralPath, probeType, method, correction, lambdaValue, secondValue,
																		number + '/')
							if not os.path.exists(outPath):
								os.makedirs(outPath)
							plot_deconv_cryst_general(
								path=crystPath,
								files=crystFiles,
								deconv=method,
								corr=correction,
								pType=probeType,
								lamb=lambdaValue,
								sec=secondValue,
								num=number,
								outPath=outPath
							)


def getData(file: str):
	data = np.loadtxt(file, delimiter = ';', dtype = 'str')
	return data


def deconv_crysts_lambda_fixed(path: str):
	deconvMethods = os.listdir(path)
	crystNumbers = ['1', '2', '3', '4']
	for method in deconvMethods:
		methodPath = os.path.join(path, method)
		probeTypes = os.listdir(methodPath)
		for probeType in probeTypes:
			probeTypePath = os.path.join(methodPath, probeType)
			correctionTypes = os.listdir(probeTypePath)
			for correction in correctionTypes:
				correctionPath = os.path.join(probeTypePath, correction)
				lambdaValues = os.listdir(correctionPath)
				for number in crystNumbers:
					for lambdaValue in lambdaValues:
						lambdaPath = os.path.join(correctionPath, lambdaValue)
						secondParamValues = os.listdir(lambdaPath)
						dataDict = {}
						for secondValue in secondParamValues:
							pathToFile = os.path.join(lambdaPath, secondValue, number, 'rectLeft.CSV')
							data = getData(file = pathToFile)
							dataDict[secondValue] = data

						outPath = os.path.join(outputRootLambdaFixed, probeType, method, correction, lambdaValue, number + '/')

						plot_deconv_cryst_lambda_fixed(
							dataDict = dataDict,
							deconv = method,
							corr = correction,
							pType = probeType,
							lamb = lambdaValue,
							num = number,
							outPath = outPath
						)


def deconv_crysts_second_fixed(path: str):
	deconvMethods = os.listdir(path)
	crystNumbers = ['1', '2', '3', '4']

	for method in deconvMethods:
		methodPath = os.path.join(path, method)
		probeTypes = os.listdir(methodPath)
		for probeType in probeTypes:
			probeTypePath = os.path.join(methodPath, probeType)
			correctionTypes = os.listdir(probeTypePath)
			for correction in correctionTypes:
				correctionPath = os.path.join(probeTypePath, correction)
				lambdaValues = os.listdir(correctionPath)
				if correction == 'asLS':
					secondValues = secondAsLSList
				else:
					secondValues = secondArLSList
				for number in crystNumbers:
					for secondValue in secondValues:
						dataDict = {}
						for lambdaValue in lambdaValues:
							pathToFile = os.path.join(correctionPath, str(lambdaValue), str(secondValue), number, 'rectLeft.CSV')
							data = getData(pathToFile)
							dataDict[lambdaValue] = data

						outPath = os.path.join(outputRootLambdaFixed, probeType, method, correction, str(secondValue), number + '/')

						plot_deconv_cryst_second_fixed(
							dataDict = dataDict,
							pType = probeType,
							num = number,
							outPath = outPath
						)
	pass
