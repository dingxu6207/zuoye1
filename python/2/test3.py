# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 10:07:46 2019

@author: dingxu
"""
import numpy as np
from skimage import io
import struct

image = io.imread('starimag.jpg')
hang,lie =  image.shape
strhang = str(hang)
strlie = str(lie)

filename = 'test.fits'
f = open(filename, "wb")

###写SIMPLE###
charsimple = [' ' for i in range(79)]
charsimple[0:8] = 'SIMPLE  ='
charsimple[29] = 'T'
strsimple = ''.join(charsimple)
encodesimple = strsimple.encode('gbk')
f.write(encodesimple)

###写BITPIX###
charbitpix = [' ' for i in range(79)]
charbitpix[0:8] = 'BITPIX  ='
charbitpix[29] = '2'
charbitpix[28] = '3'
charbitpix[27] = '-'
strbitpix = ''.join(charbitpix)
encodebitpix = strbitpix.encode('gbk')
f.write(encodebitpix)

###写NAXIS###
charNAXIS = [' ' for i in range(79)]
charNAXIS[0:8] = 'NAXIS   ='
charNAXIS[29] = '2'
strNAXIS = ''.join(charNAXIS)
encodeNAXIS = strNAXIS.encode('gbk')
f.write(encodeNAXIS)

###写NAXIS1###
charNAXIS1 = [' ' for i in range(79)]
charNAXIS1[0:8] = 'NAXIS1  ='
charNAXIS1[29] = strlie[3]
charNAXIS1[28] = strlie[2]
charNAXIS1[27] = strlie[1]
charNAXIS1[26] = strlie[0]
strNAXIS1 = ''.join(charNAXIS1)
encodeNAXIS1 = strNAXIS1.encode('gbk')
f.write(encodeNAXIS1)

###写NAXIS2###
charNAXIS2 = [' ' for i in range(79)]
charNAXIS2[0:8] = 'NAXIS2  ='
charNAXIS2[29] = strhang[3]
charNAXIS2[28] = strhang[2]
charNAXIS2[27] = strhang[1]
charNAXIS2[26] = strhang[0]
strNAXIS2 = ''.join(charNAXIS2)
encodeNAXIS2 = strNAXIS2.encode('gbk')
f.write(encodeNAXIS2)

###写EXTEND###
charEXTEND = [' ' for i in range(79)]
charEXTEND[0:8] = 'EXTEND  ='
charEXTEND[29] = 'T'
strEXTEND = ''.join(charEXTEND)
encodeEXTEND = strEXTEND.encode('gbk')
f.write(encodeEXTEND)

###写END###
charEND = [' ' for i in range(79)]
charEND[0:2] = 'END'
strEND = ''.join(charEND)
encodeEND = strEND.encode('gbk')
f.write(encodeEND)

###头文件补空格36-7=29###
charkong = [' ' for i in range(80)]
strkong = ''.join(charkong)
encodekong = strkong.encode('gbk')
for j in range(29):
    f.write(encodekong)

###转置并变成浮点数存###
#data = np.zeros((hang,lie),dtype = np.float32)
image = image.T
data = image.astype(np.float32)

for i in range(lie):
    for j in range(hang):
        dbytes = struct.pack('f',data[i][j]) #浮点数打包bytes存，读解包
        #按fits文件倒序存
        f.write(bytes([dbytes[3]]))
        f.write(bytes([dbytes[2]]))
        f.write(bytes([dbytes[1]]))
        f.write(bytes([dbytes[0]]))


###补空格(hang*lie*4+2880+x)/2880 = zheng x=1856###
dcharkong = [' ' for i in range(1856)]
dstrkong = ''.join(dcharkong)
dencodekong = dstrkong.encode('gbk')
f.write(dencodekong)
    
f.close()
