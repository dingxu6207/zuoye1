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

def makePSF(sigma):   
    hang,lie = gray.shape
    PSF = np.multiply(cv2.getGaussianKernel(hang, sigma), (cv2.getGaussianKernel(lie, sigma)).T) 
    return PSF

PSF = makePSF(sigma = 3)

 
eps = 1e-3
def make_blurred(gray, PSF, eps, coff):
    input_fft = np.fft.fft2(gray)# 进行二维数组的傅里叶变换
    PSF_fft = np.fft.fft2(PSF)+ eps
    blurred = np.fft.ifft2(input_fft * PSF_fft)
    blurredimage = np.abs(np.fft.fftshift(blurred))
    lurred_noisy = blurredimage + coff * blurredimage.std() * np.random.standard_normal(blurredimage.shape) 
    return blurredimage,lurred_noisy

blurredimage,lurred_noisy = make_blurred(gray, PSF, eps,coff = 0.5)


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
minnoise,maxnoise,inverimage = inverse(lurred_noisy, PSF, 0.4+eps)


def wiener(input,PSF,eps,K):        
    input_fft = np.fft.fft2(input)
    PSF_fft = np.fft.fft2(PSF) +eps
    PSF_fft_1 = np.conj(PSF_fft) /(np.abs(PSF_fft)**2 + K)
    result = np.fft.ifft2(input_fft * PSF_fft_1)
    result = np.abs(np.fft.fftshift(result))
    minresult = np.min(result)
    maxresult = np.max(result)
    return minresult,maxresult,result

minresult,maxresult,result = wiener(blurredimage,PSF,eps,0.01)
minwiener,maxwiener,wiener = wiener(lurred_noisy,PSF,eps,0.2)


fig = plt.figure()
ax = fig.add_subplot(241)
plt.imshow(gray, cmap = 'gray')
plt.title('Original graph')

ax = fig.add_subplot(242)
plt.imshow(blurredimage, cmap = 'gray')
plt.title('blurredimage')

ax = fig.add_subplot(243)
plt.imshow(realimage,vmin = minreal,vmax = maxreal, cmap = 'gray')
plt.title('Inverse filtering')

ax = fig.add_subplot(244)
plt.imshow(result, vmin = minresult,vmax = maxresult, cmap = 'gray')
plt.title('wienerimage')

ax = fig.add_subplot(245)
plt.imshow(lurred_noisy, cmap = 'gray')
plt.title('noiseimage')

ax = fig.add_subplot(246)
plt.imshow(inverimage, vmin = minnoise, vmax = maxnoise, cmap = 'gray')
plt.title('invernoise')

ax = fig.add_subplot(247)
plt.imshow(wiener, vmin = minwiener, vmax = maxwiener, cmap = 'gray')
plt.title('wienernoise')