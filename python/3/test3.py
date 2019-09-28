# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 22:46:30 2019

@author: dingxu
"""
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

fitsname = 'Ha_r000_20170806_090022_1B_sir.fits'
hdusir = fits.open(fitsname)
imagedatasir = hdusir[0].data

###图像显示函数###
def whadjustimage(img):
    imagedata = img
    mean = np.mean(imagedata)
    sigma = np.std(imagedata)
    mindata = np.min(imagedata)
    maxdata = np.max(imagedata)
    Imin = mean - 3*sigma
    Imax = mean + 3*sigma

    if (Imin < mindata):
        Imin = mindata
    else:
        Imin = Imin

    if (Imax > maxdata):
        Imax = maxdata
    else:
        Imax = Imax

    matdata = (imagedata-Imin)/(Imax-Imin)
    min0data = np.where(matdata < 0,0,matdata)
    min1data = np.where(min0data < 1,min0data*255,255)
    
    return np.uint8(min1data)


showsir = whadjustimage(imagedatasir)

w0 = np.array([[1,1,1],[1,1,1],[1,1,1]])*(1/9)  #均值滤波算子
w1 = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])    #锐化算子

grad = signal.convolve2d(showsir,w0,boundary='symm',mode='same')
meanfilter = np.uint8(grad)

grad1 = signal.convolve2d(showsir,w1,boundary='symm',mode='same')
suanzi = np.uint8(grad1)

G = showsir + suanzi   #增强图像
adjustimage = np.uint8(G)

fig1 = plt.figure(1)
ax1 = fig1.add_subplot(121)
ax1.imshow(showsir, cmap='gray')
plt.title('showsir')

ax1 = fig1.add_subplot(122)
ax1.imshow(meanfilter, cmap='gray')
plt.title('meanfilter')

fig2 = plt.figure(2)
ax2 = fig2.add_subplot(121)
ax2.imshow(suanzi, cmap='gray')
plt.title('suanzi')

ax2 = fig2.add_subplot(122)
ax2.imshow(adjustimage, cmap='gray')
plt.title('adjustimage')



