import numpy as np
from sklearn.neighbors import NearestNeighbors
import scipy as sc
def Generate_Structured_Data(data_files,voxel_size,grid,grid_shape): #This will output a single file with gridded data
	print('\nGenerating Structured Data')
	data = np.asarray(data_files[0])
	gridpassed = np.shape(np.shape(grid))
	if gridpassed[0] < 2:
		for file in range(1,len(data_files)):
			data = np.append(np.asarray(data_files[file]),data,axis=0)	
		data_bounds = [np.min(data[:,0]),np.max(data[:,0]),np.min(data[:,1]),np.max(data[:,1]),np.min(data[:,2]),np.max(data[:,2])]
		x_kernel_bounds = np.arange(data_bounds[0],data_bounds[1]+voxel_size,voxel_size)
		y_kernel_bounds = np.arange(data_bounds[2],data_bounds[3]+voxel_size,voxel_size)
		z_kernel_bounds = np.arange(data_bounds[4],data_bounds[5]+voxel_size,voxel_size)
		grid_meshed = np.meshgrid(x_kernel_bounds,y_kernel_bounds,z_kernel_bounds)
		grid_shape = np.shape(grid_meshed)
		grid = np.vstack(grid_meshed).reshape(3,-1).T #create list of all points in the structured grid
	print('\nTraining KNN on Pointcloud...\n')
	
	neighbors = NearestNeighbors(n_neighbors=50, algorithm='auto',n_jobs=-1).fit(data[:,0:3]) #run a knn on all the points in the pointcloud
	distances,indices = neighbors.kneighbors(grid)
	velocity_grid = np.empty(np.shape(grid)) 
	for gridpoint in range(len(grid)):
		kernel_data = data[indices[gridpoint,distances[gridpoint,:]<((voxel_size/2)*(1.8/2))],3:6]
		if len(kernel_data) >= 1:
			velocity_grid[gridpoint,:] = np.mean(kernel_data,axis=0) #average all velocity data points inside the defined radius from the structured grid point
		else:
			velocity_grid[gridpoint,:] = np.array([0,0,0])
	structured_grid = [None]
	structured_grid[0] = np.append(grid,velocity_grid,axis=1)
	return structured_grid, grid_shape

def Generate_Structured_Error_Between_Two_Datasets(data1,data2,voxel_size):
	data_bounds = [np.min(np.append(data1[:,0],data2[:,0])),np.max(np.append(data1[:,0],data2[:,0])),np.min(np.append(data1[:,1],data2[:,1])),np.max(np.append(data1[:,1],data2[:,1])),np.min(np.append(data1[:,2],data2[:,2])),np.max(np.append(data1[:,2],data2[:,2]))]
	x_kernel_bounds = np.arange(data_bounds[0],data_bounds[1]+voxel_size,voxel_size)
	y_kernel_bounds = np.arange(data_bounds[2],data_bounds[3]+voxel_size,voxel_size)
	z_kernel_bounds = np.arange(data_bounds[4],data_bounds[5]+voxel_size,voxel_size)
	grid_meshed = np.meshgrid(x_kernel_bounds,y_kernel_bounds,z_kernel_bounds)
	grid_shape = np.shape(grid_meshed)
	grid = np.vstack(grid_meshed).reshape(3,-1).T #create list of all points in the structured grid
	magdata1 = np.sqrt((data1[:,3]**2)+(data1[:,4]**2)+(data1[:,5]**2))
	magdata2 = np.sqrt((data2[:,3]**2)+(data2[:,4]**2)+(data2[:,5]**2))
	neighbors1 = NearestNeighbors(n_neighbors=500, algorithm='auto',n_jobs=-1).fit(data1[:,0:3]) #run a knn on all the points in the pointcloud
	neighbors2 = NearestNeighbors(n_neighbors=500, algorithm='auto',n_jobs=-1).fit(data2[:,0:3])
	distances1,indices1 = neighbors1.kneighbors(grid)
	distances2,indices2 = neighbors2.kneighbors(grid)
	loop_error_list = np.empty([len(grid),1])
	kernel_data1,kernel_data2 = np.empty(None),np.empty(None)
	for gridpoint in range(len(grid)):
		kernel_data1 = magdata1[indices1[gridpoint,distances1[gridpoint,:]<((voxel_size/2)*(1.8/2))]]
		kernel_data2 = magdata2[indices2[gridpoint,distances2[gridpoint,:]<((voxel_size/2)*(1.8/2))]]
		kernel_shape1,kernel_shape2 = [np.shape(kernel_data1),np.shape(kernel_data2)]
		if kernel_shape1[0] != 0 and kernel_shape2[0] != 0:
			t,p = sc.stats.ttest_ind(kernel_data1,kernel_data2,equal_var=False)
			if np.isnan(p) == True:
				loop_error_list[gridpoint,0] = 0
			else:
				loop_error_list[gridpoint,0]=p
		else:
			loop_error_list[gridpoint,0] = 0
	error_grid = np.append(grid,loop_error_list,axis=1)
	return error_grid

def Determine_Grid_Bounds_of_List_Data(list_data,voxel_size):
	print('\nDetermining Grid Bounds of List Data\n')
	data = np.asarray(list_data[0])
	data_bounds = [np.min(data[:,0]),np.max(data[:,0]),np.min(data[:,1]),np.max(data[:,1]),np.min(data[:,2]),np.max(data[:,2])]
	for image in range(0,len(list_data)):
		data = np.asarray(list_data[image])
		image_bounds = [np.min(data[:,0]),np.max(data[:,0]),np.min(data[:,1]),np.max(data[:,1]),np.min(data[:,2]),np.max(data[:,2])]
		if image_bounds[0]< data_bounds[0]: data_bounds[0]=image_bounds[0]
		if image_bounds[1]> data_bounds[1]: data_bounds[1]=image_bounds[1]
		if image_bounds[2]< data_bounds[2]: data_bounds[2]=image_bounds[2]
		if image_bounds[3]> data_bounds[3]: data_bounds[3]=image_bounds[3]
		if image_bounds[4]< data_bounds[4]: data_bounds[4]=image_bounds[4]
		if image_bounds[5]> data_bounds[5]: data_bounds[5]=image_bounds[5]
	data_bounds = [np.min(data[:,0]),np.max(data[:,0]),np.min(data[:,1]),np.max(data[:,1]),np.min(data[:,2]),np.max(data[:,2])]
	x_kernel_bounds = np.arange(data_bounds[0],data_bounds[1]+voxel_size,voxel_size)
	y_kernel_bounds = np.arange(data_bounds[2],data_bounds[3]+voxel_size,voxel_size)
	z_kernel_bounds = np.arange(data_bounds[4],data_bounds[5]+voxel_size,voxel_size)
	grid_meshed = np.meshgrid(x_kernel_bounds,y_kernel_bounds,z_kernel_bounds)
	grid = np.vstack(grid_meshed).reshape(3,-1).T #create list of all points in the structured grid
	grid_shape = np.shape(grid_meshed)
	return(grid,grid_shape)

def Translate_Data(data,x_translation,y_translation,z_translation):
	for file in range(len(data)):
		data_file = np.asarray(data[file])
		data_file[:,0] = data_file[:,0]+x_translation
		data_file[:,1] = data_file[:,1]+y_translation
		data_file[:,2] = data_file[:,2]+z_translation
		data[file] = data_file
	return data