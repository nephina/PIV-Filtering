import numpy as np
import FileReadMethods as Read
import FilteringMethods as Filter
import StructuredDataMethods as Structure
import FileWriteMethods as Write
import DisplayMethods as Show




pv3d_file_path = 'Combined.pv3d'
pv3d_folder_path = './PV3D Files/'
stl_file_path = 'PhantomMaskforMarch12thData.stl'
function_switch_list = 0,1,1,1 #turn on with 1's, in order it is Masking, Mode-filter, Median-filter, Generate Structured Data

stdev_threshold_multiplier = 2
stat_filtering_nearest_neighbor_num = 75 #how many neighbors to use to calculate the statistical model for any given point
sparse_filling_nearest_neighbor_num = 2 #keep this as low as possible, otherwise there will be far too many added points (2 is mathematically optimal, may enforce it later)
voxel_size = 0.5 #mm
hole_neighbor_level = 1
Number_Of_Modes = 1


print('Loading pv3d data...')\

data = Read.PV3D_Files(pv3d_folder_path,False,data_range=[0,24]) #generate structured grids from each raw Generate_Structured_Error_Between_Two_Datasets

	

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