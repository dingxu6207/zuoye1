# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 15:57:19 2019

@author: dingxu
"""

from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

hdu = fits.open('Mimas.fits')
imagedata = hdu[0].data

###D0截止频率，c锐化系数，Hh高频增益，Hl低频增益###
def Homomorphicfiltering(image,D0,c ,Hh,Hl): 
    ###FFT变换###
    fimagedata = np.float64(image)
    logimag = np.log(fimagedata+1)
    Fimag = np.fft.fft2(logimag)
    cenFimg = np.fft.fftshift(Fimag)

    ###滤波器###
    rows,cols = imagedata.shape
    M,N = np.meshgrid(np.arange(-cols // 2,cols // 2),np.arange(-rows//2,rows//2))
    D = np.sqrt(M ** 2 + N ** 2)
    H = (Hh - Hl) * (1 - np.exp(-c * (D ** 2 / D0 ** 2))) + Hl

    mulimage = cenFimg*H

    ###FFT反变换###
    icenimg = np.fft.ifftshift(mulimage)
    imageifft = np.fft.ifft2(icenimg)
    dstimage = np.real(imageifft)
    eimage = np.exp(dstimage)-1

    return eimage


redst = Homomorphicfiltering(imagedata ,D0 = 1024,c = 0.4 ,Hh = 2.2 ,Hl = 0.2) 
mindata = np.min(redst)
maxdata = np.max(redst)

fig = plt.figure()

ax = fig.add_subplot(121)
ax.imshow(imagedata,cmap='gray')
plt.title('Original Image')

ax = fig.add_subplot(122)
ax.imshow(redst,vmin = mindata, vmax = maxdata,cmap='gray')
plt.title('Filtered  Image')



