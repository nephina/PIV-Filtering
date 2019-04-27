import numpy as np
from scipy.io import savemat

def PV3D_File(data_files,pv3d_file_name):
	print('Writing',pv3d_file_name+'.pv3d')
	data = data_files[0]
	for file in range(len(data_files)-1):
		data = np.append(data_files[file+1],data,axis=0)
	data_shape = np.shape(data)
	with open(pv3d_file_name+'.pv3d',mode='w') as output:
		output.write('Title="'+pv3d_file_name+'" VARIABLES="X","Y","Z","U","V","W","CHC","idParticleMatchA","idParticleMatchB",DATASETAUXDATA DataType="P",DATASETAUXDATA Dimension="3",DATASETAUXDATA HasVelocity="Y",DATASETAUXDATA ExtraDataNumber="2",ZONE T="T1",I='+str(data_shape[0])+',F=POINT,\n')
		for i in range(data_shape[0]):
			output.write('\n'+str(data[i,0])+', '+str(data[i,1])+', '+str(data[i,2])+', '+str(data[i,3])+', '+str(data[i,4])+', '+str(data[i,5])+', '+str(data[i,6])+', '+str(data[i,7])+', '+str(data[i,8])+',')

def PLY_File(data_files,ply_file_name):
	print('Writing',ply_file_name+'.ply')
	data = data_files[0]
	for file in range(len(data_files)-1):
		data = np.append(data_files[file+1],data,axis=0)
	data_shape = np.shape(data)
	with open(ply_file_name+'.ply', mode='w') as output:
		output.write('ply\nformat ascii 1.0\nelement vertex '+str(data_shape[0])+'\nproperty float x\nproperty float y\nproperty float z\nproperty float nx\nproperty float ny\nproperty float nz\nend_header\n')
		for i in range(data_shape[0]):
			output.write('\n'+str(data[i,0])+' '+str(data[i,1])+' '+str(data[i,2])+' '+str(data[i,3])+' '+str(data[i,4])+' '+str(data[i,5])+'\n')

def CSV_File(data_files,csv_file_name): #this only writes the points and velocities
	print('Writing',csv_file_name+'.csv')
	data = data_files[0]
	for file in range(len(data_files)-1):
		data = np.append(data_files[file+1],data,axis=0)
	data_shape = np.shape(data)
	with open(csv_file_name+'.csv', mode='w') as output:
		output.write('"X","Y","Z","U","V","W",\n')
		for i in range(data_shape[0]):
			output.write('\n'+str(data[i,0])+', '+str(data[i,1])+', '+str(data[i,2])+', '+str(data[i,3])+', '+str(data[i,4])+', '+str(data[i,5])+',')

def CSV_Mag_File(data_files,csv_file_name): #this only writes the points and velocities
	print('Writing',csv_file_name+'.csv')
	data = data_files[0]
	for file in range(len(data_files)-1):
		data = np.append(data_files[file+1],data,axis=0)
	data_shape = np.shape(data)
	with open(csv_file_name+'.csv', mode='w') as output:
		output.write('"Magnitude",')
		for i in range(data_shape[0]):
			output.write('\n'+str(data[i])+',')

def MAT_File(data_files,mat_file_name):
	print('Writing',mat_file_name+'.mat')
	data = data_files[0]
	for file in range(len(data_files)-1):
		data = np.append(data_files[file+1],data,axis=0)
	data_shape = np.shape(data)
	savemat(mat_file_name,dict['data',data])