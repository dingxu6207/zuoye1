# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:40:20 2019
@author: dingxu
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import data

gray = data.camera()

hang,lie = gray.shape
sigma = 3
def makePSF(sigma):    
    PSF = np.multiply(cv2.getGaussianKernel(hang, sigma), (cv2.getGaussianKernel(lie, sigma)).T) 
    return PSF

PSF = makePSF(sigma)


eps = 0.0001
def make_blurred(gray, PSF, eps):
    input_fft = np.fft.fft2(gray)# 进行二维数组的傅里叶变换
    PSF_fft = np.fft.fft2(PSF)+ eps
    blurred = np.fft.ifft2(input_fft * PSF_fft)
    blurredimage = np.abs(np.fft.fftshift(blurred))
    return blurredimage

blurredimage = make_blurred(gray, PSF, eps)


def inverse(blurredimage, PSF, eps):
    fftgray = np.fft.fft2(blurredimage)
    fftPSF = np.fft.fft2(PSF)
    divimg = fftgray/(fftPSF+eps)#逆滤波
    ifftimg = np.fft.ifft2(divimg)
    realimage = np.abs(np.fft.fftshift(ifftimg))
    minreal = np.min(realimage)
    maxreal = np.max(realimage)
    return minreal,maxreal,realimage

minreal,maxreal,realimage = inverse(blurredimage, PSF, eps)



def wiener(input,PSF,eps,K = 0.001):        #维纳滤波，K=0.01
    input_fft = np.fft.fft2(input)
    PSF_fft = np.fft.fft2(PSF) +eps
    PSF_fft_1 = np.conj(PSF_fft) /(np.abs(PSF_fft)**2 + K)
    result = np.fft.ifft2(input_fft * PSF_fft_1)
    result = np.abs(np.fft.fftshift(result))
    minresult = np.min(result)
    maxresult = np.max(result)
    return minresult,maxresult,result

minresult,maxresult,result = wiener(blurredimage,PSF,eps)



fig = plt.figure()
ax = fig.add_subplot(221)
ax.imshow(gray, cmap = 'gray')
plt.title('Original graph')

ax = fig.add_subplot(222)
plt.imshow(blurredimage, cmap = 'gray')
plt.title('blurredimage')

ax = fig.add_subplot(223)
plt.imshow(realimage,vmin = minreal,vmax = maxreal, cmap = 'gray')
plt.title('Inverse filtering')

ax = fig.add_subplot(224)
plt.imshow(result, vmin = minresult,vmax = maxresult, cmap = 'gray')
plt.title('wienerimage')

