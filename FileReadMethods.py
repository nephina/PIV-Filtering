import numpy as np
import os,fnmatch,csv
import StructuredDataMethods as Structure

def PV3D_Files(folder_path,single_file_switch,data_range): # If only a single file is being read, data_range does nothing
	if single_file_switch == True:
		file_name = folder_path
		data = [None]
		print('reading '+str(file_name))
		data[0] = (np.genfromtxt(file_name, dtype=np.float64, delimiter=',',skip_header=1,usecols=(0,1,2,3,4,5,6,7,8))).tolist()
		return data
	else:
		file_names = fnmatch.filter(sorted(os.listdir(folder_path)),'*pv3d')
		data = [None] * (data_range[1]-data_range[0])
		for file in range(data_range[0],data_range[1]):
			print('reading '+file_names[file])
			data[file-data_range[0]] = (np.genfromtxt(folder_path+file_names[file], dtype=np.float64, delimiter=',',skip_header=1,usecols=(0,1,2,3,4,5,6,7,8))).tolist()
		return data

def PV3D_Files_Into_Structured_Grid(voxel_size,folder_path,data_range):
	file_names = fnmatch.filter(sorted(os.listdir(folder_path)),'*pv3d')
	data = [None] * (data_range[1]-data_range[0])
	data_file = [None]
	for file in range(0,(data_range[1]-data_range[0])):
		print('reading '+file_names[file])
		data_file[0] = np.genfromtxt(folder_path+file_names[file], dtype=np.float64, delimiter=',',skip_header=1,usecols=(0,1,2,3,4,5,6,7,8))
		list_format_data,grid_shape = Structure.Generate_Structured_Data(data_file,voxel_size,0,0)
		data[file] = list_format_data[0]
		data_file = [None]
	return data

def CSV_Files(folder_path,data_range): #needs testing
	file_names = fnmatch.filter(sorted(os.listdir(folder_path)),'*pv3d')
	data = [None] * (data_range[1]-data_range[0])
	for file in range(data_range[0],data_range[1]):
		print('reading '+file_names[file])
		data[file-data_range[0]] = (np.genfromtxt(folder_path+file_names[file], dtype=np.float64, delimiter=',',skip_header=1,usecols=(0,1,2,3,4,5,6,7,8))).tolist()
	return data
