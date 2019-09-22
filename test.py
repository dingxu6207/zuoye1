# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from astropy.io import fits
import numpy as np
import math
from skimage import io

hdu = fits.open('E:/MATLABTEST/zuoye/matlab/1/201906061616150716.fit')
imgdata = hdu[0].data


########################################
##拉伸对比度
rows,cols = imgdata.shape

minimagedata = imgdata.min()
maximagedata = imgdata.max()

for i in range(rows):
    for j in range(cols):
        if (imgdata[i,j] > maximagedata):
            imgdata[i,j] = 255
        elif (imgdata[i,j] < minimagedata):
            imgdata[i,j] = 0
        else:
            imgdata[i,j] = 255*((imgdata[i,j] - minimagedata)/(maximagedata - minimagedata))
            
          
#u8imagedata = exposure.adjust_gamma(u8imagedata, 0.3)
u8imagedata = (255/math.log(256))*np.log(1+imgdata)
u8imagedata = np.uint8(u8imagedata)  

io.imsave('E:/MATLABTEST/zuoye/starimag.jpg',u8imagedata)

