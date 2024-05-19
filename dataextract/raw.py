from graph.raw import *
sourceDataDir = "/home/sewik/source/repos/Spectra/data"
rootDataDir = "/home/sewik/source/repos/CrystAnalysisKit/data"
rootImageDir = "/home/sewik/source/repos/CrystAnalysisKit/images"
calcTypes = ['raw']


def separate_crysts(fileList, path):
	crystDictionary = {
		'1': np.array([], dtype='str'),
		'2': np.array([], dtype='str'),
		'3': np.array([], dtype='str'),
		'4': np.array([], dtype='str')
	}
	for file in fileList:
		if file.__contains__("cryst1"):
			crystDictionary['1'] = np.append(crystDictionary['1'], path + file)
		if file.__contains__("cryst2"):
			crystDictionary['2'] = np.append(crystDictionary['2'], path + file)
		if file.__contains__("cryst3"):
			crystDictionary['3'] = np.append(crystDictionary['3'], path + file)
		if file.__contains__("cryst4"):
			crystDictionary['4'] = np.append(crystDictionary['4'], path + file)
	return crystDictionary


def raw_cryst_general():
	probeTypes = []
	bgCorrMethodDirPath = ""
	bgCorrMethod = ""
	for calcType in calcTypes:
		calcTypeDirPath = os.path.join(rootDataDir, calcType)
		bgCorrMethods = os.listdir(calcTypeDirPath)
		for bgCorrMethod in bgCorrMethods:
			bgCorrMethodDirPath = os.path.join(calcTypeDirPath, bgCorrMethod)
			probeTypes = os.listdir(bgCorrMethodDirPath)
		for probeType in probeTypes:
			probeTypeDirPath = os.path.join(bgCorrMethodDirPath, probeType)
			lambdaValues = os.listdir(probeTypeDirPath)
			for lambdaValue in lambdaValues:
				lambdaValueDirPath = os.path.join(probeTypeDirPath, lambdaValue)
				crystList = os.listdir(lambdaValueDirPath)
				separatedCrysts = separate_crysts(crystList, lambdaValueDirPath)
				for crystNumber, fileList in separatedCrysts.items():
					for dataFile in fileList:
						pathToFile = os.path.join(lambdaValueDirPath, dataFile)
						secondParamValue = dataFile.split('-')[3]
						names, values = get_data(filePath=pathToFile)
						pathToSave = os.path.join(rootImageDir, calcType, probeType, lambdaValue, bgCorrMethod, 'general/')
						plot_raw(
							names,
							values,
							str(probeType[0]).upper(),
							correctMethod = bgCorrMethod,
							crystNum = crystNumber,
							lambdaValue = lambdaValue,
							secondParam = secondParamValue,
							pathToSave = pathToSave
						)


def raw_cryst_lambda_fixed():
	calcTypeDirPath = os.path.join(rootDataDir, calcTypes[0])
	correctionMethods = os.listdir(calcTypeDirPath)
	for correctionMethod in correctionMethods:
		correctionDirPath = os.path.join(calcTypeDirPath, correctionMethod)
		probeTypes = os.listdir(correctionDirPath)
		for probeType in probeTypes:
			probeTypeDirPath = os.path.join(correctionDirPath, probeType)
			lambdaValues = os.listdir(probeTypeDirPath)
			probeNames = get_probe_names(sourceDataDir, probeType)
			for lambdaValue in lambdaValues:
				crystsPath = os.path.join(probeTypeDirPath, lambdaValue + '/')
				crystList = os.listdir(crystsPath)
				crystsDict = separate_crysts(crystList, crystsPath)
				for crystNum, fileList in crystsDict.items():
					crystsContentDict = get_data_files_content_dict(crystsPath, fileList)
					pathToSave = os.path.join(rootImageDir, 'lambdaFixed', probeType, lambdaValue, correctionMethod + '/')
					plot_raw_lambda_fixed(crystsContentDict, probeType[0].upper(), probeNames, correctionMethod, crystNum, pathToSave)


def raw_cryst_second_fixed():
	calcTypeDirPath = os.path.join(rootDataDir, calcTypes[0])
	correctionMethods = os.listdir(calcTypeDirPath)
	for correctionMethod in correctionMethods:
		correctionDirPath = os.path.join(calcTypeDirPath, correctionMethod)
		probeTypes = os.listdir(correctionDirPath)
		for probeType in probeTypes:
			probeTypeDirPath = os.path.join(correctionDirPath, probeType)
			lambdaValues = os.listdir(probeTypeDirPath)
			crystsAccumulatedDictFiles = {}
			probeNames = get_probe_names(sourceDataDir, probeType)
			for lambdaValue in lambdaValues:
				crystsPath = os.path.join(probeTypeDirPath, lambdaValue + '/')
				crystList = os.listdir(crystsPath)
				crystsDict = separate_crysts(crystList, crystsPath)
				crystsAccumulatedDictFiles[lambdaValue] = crystsDict
			# crystsAccumulatedDictData = extract_raw_for_second_fixed(crystsAccumulatedDictFiles)
			pathToSave = os.path.join(rootImageDir, 'secondFixed', probeType)
			plot_raw_second_fixed(crystsAccumulatedDictFiles, probeNames, correctionMethod, probeType[0].upper(), pathToSave)
