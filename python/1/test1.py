# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 16:43:18 2019

@author: dingxu
"""
from skimage import io
import matplotlib.pyplot as plt
import math


##################################
##函数实现最大值、最小值、平均和标准差

def solvevalue(temphang,lie):
    sum1 = 0.0
    sum2 = 0.0
    maxdata = temphang[0]
    mindata = temphang[0]
    flag = True 
    
    i = 0
    while i < lie:
        if flag == True:
            if (maxdata < temphang[i]):
                maxdata = temphang[i]
            
            if (mindata > temphang[i]): 
                mindata = temphang[i]
            
            sum1 += temphang[i]
        
            if i == (lie - 1):
               meandata = sum1/lie 
               flag = False   
               i = 0
               
       
        if flag == False:  
            chapinjundata = temphang[i] - meandata            
            sunchapinjun = chapinjundata**2
            sum2 += sunchapinjun
        
        i = i+1
            
    chulie = sum2/lie  
    stddata = math.sqrt(chulie)
        
    return maxdata,mindata,meandata,stddata


####################################
##读图像并调用函数    
image = io.imread('starimag.jpg')
hang,lie =  image.shape

#定义数组
arrtemphang = [0 for i in range(lie)] 
arrmeandata = [0 for i in range(lie)]    
arrstddata =  [0 for i in range(lie)]     
arrmaxdata =  [0 for i in range(lie)]     
arrmindata =  [0 for i in range(lie)]     


for i in range(hang):
    arrtemphang = image[i,:]
    maxdata,mindata,meandata,stddata = solvevalue(arrtemphang,lie)    
    arrmaxdata[i] = maxdata
    arrmindata[i] = mindata
    arrmeandata[i] = meandata
    arrstddata[i] = stddata


###########################
##显示 

fig = plt.figure()   
ax = fig.add_subplot(511)  
io.imshow(image) 

ax = fig.add_subplot(512) 
plt.plot(arrmaxdata)

ax = fig.add_subplot(513) 
plt.plot(arrmindata)

ax = fig.add_subplot(514) 
plt.plot(arrmeandata)

ax = fig.add_subplot(515) 
plt.plot(arrstddata)

plt.show()

