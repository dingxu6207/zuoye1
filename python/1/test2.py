# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 10:06:51 2019

@author: dingxu
"""
from skimage import io
import matplotlib.pyplot as plt
import numpy as np

image = io.imread('starimag.jpg')
hang,lie =  image.shape

onedata = np.ones((hang,1))
sumdata = np.dot(image,onedata)
meandata = sumdata/lie         #平均值

datacha = image - meandata
pingfangdata = datacha**2
sumdata = np.dot(pingfangdata,onedata)
nsumdata = sumdata/lie
sigmadata = np.sqrt(nsumdata) #标准差


#############################################
##求最大和最小值
maxdata = image[:,0]
mindata = image[:,0]

for i in range(lie):
    maxdata = np.maximum(maxdata,image[:,i])
    mindata = np.minimum(mindata,image[:,i])
  
    
#############################################
##显示
    
fig = plt.figure()   
ax = fig.add_subplot(511)  
io.imshow(image) 

ax = fig.add_subplot(512) 
plt.plot(maxdata)

ax = fig.add_subplot(513) 
plt.plot(mindata)

ax = fig.add_subplot(514) 
plt.plot(meandata)

ax = fig.add_subplot(515) 
plt.plot(sigmadata)

plt.show()  