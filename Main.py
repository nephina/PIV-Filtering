import numpy as np
import FileReadMethods as Read
import FilteringMethods as Filter
import StructuredDataMethods as Structure
import FileWriteMethods as Write
import DisplayMethods as Show




pv3d_file_path = 'Combined.pv3d'
pv3d_folder_path = '/home/alexa/Dropbox/MCW009Phantom/PIV Data/March12thRun/PV3D Slice Files/'
stl_file_path = 'PhantomMaskforMarch12thData.stl'
function_switch_list = 0,0,0,1 #turn on with 1's, in order it is Masking, Mode-filter, Median-filter, Generate Structured Data

stdev_threshold_multiplier = 2
stat_filtering_nearest_neighbor_num = 75 #how many neighbors to use to calculate the statistical model for any given point
sparse_filling_nearest_neighbor_num = 2 #keep this as low as possible, otherwise there will be far too many added points (2 is mathematically optimal, may enforce it later)
voxel_size = 0.5 #mm
hole_neighbor_level = 1
Number_Of_Modes = 1


print('Loading pv3d data...')
#data = np.genfromtxt(pv3d_file_path, dtype=np.float64, delimiter=',',skip_header=1,usecols=(0,1,2,3,4,5,6,7,8))
#data1 = Read.PV3D_Files(pv3d_folder_path, combine_data=True,data_range=[0,500]) #read the raw data
#data1Mag = np.sqrt((data1[:,3]*data1[:,3])+(data1[:,4]*data1[:,4])+(data1[:,5]*data1[:,5]))
#data2 = Read.PV3D_Files(pv3d_folder_path, combine_data=True,data_range=[500,1000])
#data2Mag = np.sqrt((data1[:,3]*data1[:,3])+(data1[:,4]*data1[:,4])+(data1[:,5]*data1[:,5]))
#data3 = Read.PV3D_Files(pv3d_folder_path, combine_data=True,data_range=[1000,1500])
#data3Mag = np.sqrt((data1[:,3]*data1[:,3])+(data1[:,4]*data1[:,4])+(data1[:,5]*data1[:,5]))

#sdelta1to2 = np.sqrt(((np.std(data1)*np.std(data1))/len(data1))+((np.std(data2)*np.std(data2))/len(data2)))
#Tstatistic1to2 = (np.mean(data1)-np.mean(data2))/sdelta1to2
#print(Tstatistic1to2)

#sdelta2to3 = np.sqrt(((np.std(data2)*np.std(data2))/len(data2))+((np.std(data3)*np.std(data3))/len(data3)))
#Tstatistic2to3 = (np.mean(data2)-np.mean(data3))/sdelta2to3
#print(Tstatistic2to3)

#sdelta1to3 = np.sqrt(((np.std(data1)*np.std(data1))/len(data1))+((np.std(data3)*np.std(data3))/len(data3)))
#Tstatistic1to3 = (np.mean(data1)-np.mean(data3))/sdelta1to3
#print(Tstatistic1to3)

data = Read.PV3D_Files("ModeFiltered.pv3d",True,data_range=[0,19]) #generate structured grids from each raw Generate_Structured_Error_Between_Two_Datasets
#Write.MAT_File(data,"MATsavetesting")
#data = np.empty([1,9])
#for file in range(len(data1)):
#	data = np.append(data,data1[file],axis=0)
#	print(file,np.shape(data))
#mag1 = np.sqrt((data1[:,3]*data1[:,3])+(data1[:,4]*data1[:,4])+(data1[:,5]*data1[:,5]))
#mag1 = np.log(mag1/(1-(2.45*mag1)))
#data2 = Read.PV3D_Files(pv3d_folder_path,combine_data=True,data_range=[500,1000]) #generate structured grids from each raw dataset
#mag2 = np.sqrt((data2[:,3]*data2[:,3])+(data2[:,4]*data2[:,4])+(data2[:,5]*data2[:,5]))
#mag2 = np.log(mag2/(1-(2.45*mag2)))
#data3 = Read.PV3D_Files(pv3d_folder_path,combine_data=True,data_range=[1000,1500]) #generate structured grids from each raw dataset
#mag3 = np.sqrt((data3[:,3]*data3[:,3])+(data3[:,4]*data3[:,4])+(data3[:,5]*data3[:,5]))
#mag3 = np.log(mag3/(1-(2.45*mag3)))
#Write.CSV_Mag_File(mag1,'SampleRun1')
#Write.CSV_Mag_File(mag2,'SampleRun2')
#Write.CSV_Mag_File(mag3,'SampleRun3')
#data = Filter.Remove_Outliers(Read.PV3D_Files(pv3d_folder_path,combine_data=False,data_range=[0,500]))
#data1 = Read.PV3D_Files(pv3d_folder_path,combine_data=True,data_range=[0,100])
#data2 = Read.PV3D_Files(pv3d_folder_path,combine_data=True,data_range=[500,600])
#Show.Individual_Images(data1)
#Show.Magnitude_Normality_Plots(data)
#error_grid = Structure.Generate_Structured_Error_Between_Two_Datasets(data1,data2,1)
#Show.Error_Plot(error_grid)
#error_grid = Structure.Generate_Structured_Error_Between_Two_Datasets(data2,data3,1)
#Show.Error_Plot(error_grid)
#error_grid = Structure.Generate_Structured_Error_Between_Two_Datasets(data1,data3,1)
#Show.Error_Plot(error_grid)
	

if function_switch_list[0] == 1:
	data = Filter.Geometry_Mask_ImplicitPolyDataDistance(data,stl_file_path)
	Write.PLY_File(data,'Masked')
	Write.PV3D_File(data,'Masked')
if function_switch_list[1] == 1:
	data = Filter.Mode_Filtering(data,stat_filtering_nearest_neighbor_num,stdev_threshold_multiplier)
	Write.PLY_File(data,'ModeFiltered')
	Write.PV3D_File(data,'ModeFiltered')
if function_switch_list[2] == 1:
	data = Filter.Median_Filtering(data,stat_filtering_nearest_neighbor_num,stdev_threshold_multiplier)
	Write.PLY_File(data,'MedianFiltered')
	Write.PV3D_File(data,'MedianFiltered')
if function_switch_list[3] == 1:
	data,grid_shape = Structure.Generate_Structured_Data(data,voxel_size,0,0)
	Write.PLY_File(data,'StructuredData(FilteredandMasked)'+str(grid_shape[::-1]))
	Write.CSV_File(data,'StructuredData(FilteredandMasked)'+str(grid_shape[::-1]))

#Write.PV3D_File(data,'00CombinedPV3D')
#Write.PLY_File(data,'00CombinedPV3D')
#Write.PV3D_File(Structure.Translate_Data(data,0,0,-17.6),'18CombinedPV3D')
#Write.PLY_File(Structure.Translate_Data(data,0,0,-17.6),'18CombinedPV3D')

#data,grid_shape = Filter.SVD_Of_Imageset(data,Number_Of_Modes,voxel_size)
#data = np.asarray(data)
#data = np.append(data[0,:,0:3],np.sum(data[:,:,3:6],axis = 0),axis = 1)
#Write.CSV_File([data],'SVDMode1'+str(grid_shape[::-1]))

print("\ndone")