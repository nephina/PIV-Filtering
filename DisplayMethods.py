import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import axes3d
import scipy as sc

def Individual_Images(data): #data must come in in list format
	plt.ion()
	fig = plt.figure()
	ax = fig.gca(projection="3d")
	fig_manager = plt.get_current_fig_manager()
	#fig_manager.window.showMaximized()
	for image in range(0,len(data)):
		plt.cla()
		data_slice = np.asarray(data[image])
		ax.quiver(data_slice[:,0],-data_slice[:,2],data_slice[:,1],data_slice[:,3],data_slice[:,4],data_slice[:,5],	normalize=True)
		#ax.set_xlim(left=450,right=500)
		#ax.set_ylim(bottom=450,top=500)
		#ax.set_zlim(bottom=-25,top=25)
		plt.draw()
		plt.pause(1)
		print('Image #'+str(image+1))
	plt.close()

def Error_Plot(data): #data should come in single structured grid
	pmax,pmin = np.max(data[:,3]),np.min(data[:,3])
	prange = pmax-pmin
	normalized_prange = (data[:,3]-pmin)/prange
	color = np.transpose(np.vstack((np.vstack((np.vstack((normalized_prange,np.zeros(len(data)))),1-normalized_prange)),normalized_prange)))
	print(np.shape(color))
	fig = plt.figure()
	ax = fig.add_subplot(111,projection="3d")
	ax.scatter(data[:,0],-data[:,2],data[:,1],c=color)
	ax.set_xlim(left=450,right=500)
	ax.set_ylim(bottom=450,top=500)
	ax.set_zlim(bottom=-25,top=25)
	plt.show()

def Velocity_Histograms(data): #data must come in in list format
	plt.ion()
	fig = plt.figure()
	fig_manager = plt.get_current_fig_manager()
	fig_manager.window.showMaximized()
	for image in range(0,len(data)):
		plt.clf()
		data_slice = np.asarray(data[image])
		plt.hist(np.sqrt((data_slice[:,3]*data_slice[:,3])+(data_slice[:,4]*data_slice[:,4])+(data_slice[:,5]*data_slice[:,5])),bins=1000,histtype='step',density=True,cumulative=True)
		plt.ylim(top=1)
		plt.xlim(left=0,right=0.5)
		#plt.xscale("log")
		#plt.yscale("log")
		#for velocity_dim in range(3):
		#	plt.subplot(1,3,velocity_dim+1)
		#	plt.hist(data_slice[:,(velocity_dim+3)],bins=500,histtype='step')
		#	plt.ylim(top=100)
		#	plt.xlim(left=-0.5,right=0.5)
		plt.draw()
		plt.pause(0.001)

def Magnitude_Normality_Plots(data): #data must come in in list format
	plt.ion()
	fig = plt.figure()
	fig_manager = plt.get_current_fig_manager()
	for image in range(0,len(data)):
		data_slice = np.asarray(data[image])
		plotdata = np.sqrt((data_slice[:,3]*data_slice[:,3])+(data_slice[:,4]*data_slice[:,4])+(data_slice[:,5]*data_slice[:,5]))
		transformedplotdata = np.log(plotdata/(1-(2.45*plotdata)))
		results = sc.stats.probplot(transformedplotdata,plot=plt)
		r = results[1][2]
		t_score = r/((1-(r**2))/(len(plotdata)-2))
		p_value = sc.stats.t.cdf(t_score,len(plotdata)-1)
		plt.ylim(top=4,bottom=-8)
		plt.xlim(left=-4,right=4)
		plt.draw()
		plt.pause(0.01)
	plt.pause(5)