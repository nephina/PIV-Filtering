import StructuredDataMethods as Structure
from sklearn.neighbors import NearestNeighbors
import numpy as np
import os,fnmatch,csv
import vtk
import scipy as sc

def Geometry_Mask_ImplicitPolyDataDistance(data,stl_file_path): #returns list of all PIV images
	print('\nFiltering Using Manifold Surface')
	print("\nReading STL File...")
	meshReader = vtk.vtkSTLReader()
	meshReader.SetFileName(stl_file_path)
	meshReader.Update()
	polydata = meshReader.GetOutput()
	implicit_function = vtk.vtkImplicitPolyDataDistance()
	implicit_function.SetInput(polydata)
	masked_data = [None]*len(data)
	print("\nMasking points...\n")
	for file in range(len(data)):
		data_file = np.array(data[file])
		data_shape = np.shape(data_file)
		points = data_file[:,0:3] #these are the data points you want to mask, you can pass any number of point attributes in "data" as long as the point locations are in the first three indices of each row
		mask_indices = np.zeros(data_shape[0])
		for point in range(data_shape[0]):
			if (implicit_function.FunctionValue(points[point,:]) <= 0):
				mask_indices[point] = 1
		masked_data[file] = data_file[(mask_indices != 0),:] #pull all points that passed the test into a new matrix
	return masked_data

def Mode_Filtering(data,stat_filtering_nearest_neighbor_num,stdev_threshold_multiplier):
	print('\nFiltering by Mode')
	data_blob = data[0]
	for file in range(len(data)-1):
		data_blob = np.append(data[file+1],data_blob,axis=0)
	print('There are '+str(len(data_blob))+' vectors to analyze')
	data_shape = np.shape(data_blob)
	file_index_regions = [None]*(len(data)+1)
	overall_length = 0
	for file in range(len(data)):
		file_index_regions[file] = overall_length
		overall_length = len(data[file])+overall_length
		file_index_regions[file+1] = overall_length
	print('\nTraining KNN on Pointcloud...')
	points = data_blob[:,0:3]
	neighbors = NearestNeighbors(n_neighbors=stat_filtering_nearest_neighbor_num, algorithm='auto',n_jobs=-1).fit(points) #run a knn on all the points in the pointcloud
	distances,indices = neighbors.kneighbors(points) #use the knn results back on the same pointcloud, generating a group of nearest neighboring points for every point in the pointcloud
	print('\nStatistical Analysis...')
	velocity_std_dev = stdev_threshold_multiplier*np.std(data_blob[indices,3:6],axis=1) #find the standard deviation of the velocity data for individual x,y,z components
	velocity_mode = np.empty((data_shape[0],3))
	for point in range(data_shape[0]):
		for axis in range(3):
			point_axis_hist = np.histogram(data_blob[indices[point],3:6],100)
			hist_count = point_axis_hist[0]
			hist_bins = point_axis_hist[1]
			velocity_mode[point,axis] = hist_bins[np.argmax(hist_count)]
	print('\nTesting Points...\n')
	exclusion_velocity = 0.1
	pass_index = np.empty(data_shape[0],dtype=int)
	for i in range(int(data_shape[0])):
		if data_blob[i,3] > (velocity_mode[i,0]-velocity_std_dev[i,0]) and data_blob[i,3] < (velocity_mode[i,0]+velocity_std_dev[i,0]) and data_blob[i,4] > (velocity_mode[i,1]-velocity_std_dev[i,1]) and data_blob[i,4] < (velocity_mode[i,1]+velocity_std_dev[i,1]) and data_blob[i,5] > (velocity_mode[i,2]-velocity_std_dev[i,2]) and data_blob[i,5] < (velocity_mode[i,2]+velocity_std_dev[i,2]): # the data that passes must lie close enough to the mode in every dimension that it is within n standard deviation, n defined by user
			pass_index[i] = i
		else:
			pass_index[i] = 0
	filtered_data = [None]*len(data)
	print('There are '+str(len(pass_index[pass_index!=0]))+' vectors left')
	for file in range(len(data)):
		file_pass_index = pass_index[file_index_regions[file]:file_index_regions[file+1]]-file_index_regions[file]
		file_pass_index = file_pass_index[file_pass_index>0]
		individual_file = np.asarray(data[file])
		filtered_data[file] = individual_file[file_pass_index,:]
	return filtered_data

def Median_Filtering(data,stat_filtering_nearest_neighbor_num,stdev_threshold_multiplier):
	print('\nFiltering by Median')
	data_blob = data[0]
	for file in range(len(data)-1):
		data_blob = np.append(data[file+1],data_blob,axis=0)
	data_shape = np.shape(data_blob)
	file_index_regions = [None]*(len(data)+1)
	overall_length = 0
	for file in range(len(data)):
		file_index_regions[file] = overall_length
		overall_length = len(data[file])+overall_length
		file_index_regions[file+1] = overall_length
	points = data_blob[:,0:3]
	data_shape = np.shape(data_blob)
	print('\nTraining KNN on Pointcloud...')
	neighbors = NearestNeighbors(n_neighbors=stat_filtering_nearest_neighbor_num, algorithm='auto',n_jobs=-1).fit(points) #run a knn on all the points in the pointcloud
	distances,indices = neighbors.kneighbors(points) #use the knn results back on the same pointcloud, generating a group of nearest neighboring points for every point in the pointcloud
	print('\nStatistical Analysis...')
	velocity_std_dev = stdev_threshold_multiplier*np.std(data_blob[indices,3:6],axis=1) #find the standard deviation of the velocity data for individual x,y,z components
	velocity_median = np.median(data_blob[indices,3:6],axis=1) #find the median of the velocity data for individual x,y,z components
	print('\nTesting Points...\n')
	pass_index = np.empty(data_shape[0],dtype=int)
	for i in range(int(data_shape[0])):
		if data_blob[i,3] > (velocity_median[i,0]-velocity_std_dev[i,0]) and data_blob[i,3] < (velocity_median[i,0]+velocity_std_dev[i,0]) and data_blob[i,4] > (velocity_median[i,1]-velocity_std_dev[i,1]) and data_blob[i,4] < (velocity_median[i,1]+velocity_std_dev[i,1]) and data_blob[i,5] > (velocity_median[i,2]-velocity_std_dev[i,2]) and data_blob[i,5] < (velocity_median[i,2]+velocity_std_dev[i,2]): # the data that passes must lie close enough to the median in every dimension that it is within n standard deviation, n defined by user
			pass_index[i] = i
		else:
			pass_index[i] = 0
	filtered_data = [None]*len(data)
	for file in range(len(data)):
		file_pass_index = pass_index[file_index_regions[file]:file_index_regions[file+1]]-file_index_regions[file]
		file_pass_index = file_pass_index[file_pass_index>0]
		individual_file = np.asarray(data[file])
		filtered_data[file] = individual_file[file_pass_index,:]
	return filtered_data

#def RBF_Based_Filtering(data):

#def Fill_Sparse_Areas(data,sparse_filling_nearest_neighbor_num,min_distance_parameter):

def SVD_Of_Imageset(data,Number_Of_Modes,voxel_size):
	grid, grid_shape = Structure.Determine_Grid_Bounds_of_List_Data(data,voxel_size)
	structured_data = [None]*len(data)
	list_format = [None]
	for file in range(len(data)):
		print("\nStructuring image #"+str(file+1))
		list_format[0] = data[file]
		list_format_data,grid_shape = Structure.Generate_Structured_Data(list_format,voxel_size,grid,grid_shape)	
		structured_data[file] = list_format_data[0]
	data_shape = np.shape(structured_data[0])
	image_vectors = np.empty([data_shape[0]*3,len(data)])
	for ImageNumber in range(len(data)):
		image_data = structured_data[ImageNumber]
		image_vectors[:,ImageNumber] = np.ravel(image_data[:,3:6],"F") #ravel/vectorize each 3D image(vector field) to 1D and insert into the 2D matrix "image_vectors"
	print("\n-----------------Performing Sparse SVD Algorithm-------------------\n")
	u, s, v = sc.sparse.linalg.svds(sc.sparse.csr_matrix.asfptype(image_vectors),k=Number_Of_Modes,which='LM')
	um,sm,vm = np.asmatrix(u),np.asmatrix(s),np.asmatrix(v) #move to matrix data type for processing
	del u,s,v #memory management
	ModeList = [None]*Number_Of_Modes #initialization before loop
	ImageVelocityComponent = [None]
	for mode in range(Number_Of_Modes):
		Mode  = np.mean(np.array(um[:,mode] * sm[:,mode] * vm[mode,:]),axis=1) 
		ModeList[mode] = np.append(grid,np.reshape(Mode,[data_shape[0],3],order="F"),axis=1) #reshape the modes back into a stack of 3D vector fields
	return(ModeList,grid_shape)