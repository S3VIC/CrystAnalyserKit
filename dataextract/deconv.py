from graph.deconvCrysts import *

outputRootGeneralPath = "/home/sewik/source/repos/CrystAnalyserKit/images/deconvGeneral"


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
