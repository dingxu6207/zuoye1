# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 10:04:33 2019

@author: dingxu
"""

from astropy.io import fits
import matplotlib.pyplot as plt


hdu = fits.open('test.fits')
hdu.info()
print(hdu[0].header)
hdudata = hdu[0].data
plt.imshow(hdudata, cmap='gray')