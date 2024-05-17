import os
import numpy as np


def get_data(filePath):
	content = np.loadtxt(fname = filePath, delimiter = "$", dtype='str')
	names = np.array(content[:, 0])
	values = np.array(content[:, 1])
	return validate_data(names, values)


def validate_data(names, values):
	emptyCrystIndexes = np.where(values == '')
	for index in emptyCrystIndexes:
		values = np.delete(values, index)
		names = np.delete(names, index)
	return names, values


def separate_second_params_list(fileList: list[str]):
	values = np.array([], dtype=float)
	for file in fileList:
		value = float(file.split('-')[3])
		if not values.__contains__(value):
			values = np.append(values, value)
	return values


def get_probe_names(rootDataPath: str, probeType: str):
	finalPath = os.path.join(rootDataPath, probeType, 'csvCombined/')
	allFilesList = os.listdir(finalPath)
	dataFileList = np.array([], dtype = 'str')
	for file in allFilesList:
		if file[-4:].upper() != '.CSV':
			continue
		dataFileList = np.append(dataFileList, file[:-4])

	return dataFileList


def get_data_files_content_dict(path: str, fileList):
	contentDict = {}
	for file in fileList:
		content = np.loadtxt(path + file, delimiter = '$', dtype = 'str')
		contentDict[file.split('-')[3]] = content
	return contentDict
