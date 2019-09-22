# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 10:07:46 2019

@author: dingxu
"""
import numpy as np
from skimage import io
import struct
import math

image = io.imread('starmin.jpg')
imageT = image.T
hang,lie =  imageT.shape
strhang = str(hang)
strlie = str(lie)

filename = 'test.fits'
f = open(filename, "wb")

###写NAXIS长度###
def writeNAXISleng(listNAXIS,strtemp):
    length = len(strtemp)
    if (length == 4):
        listNAXIS[29] = strtemp[3]    
        listNAXIS[28] = strtemp[2]
        listNAXIS[27] = strtemp[1]
        listNAXIS[26] = strtemp[0]
    if (length == 3):
        listNAXIS[29] = strtemp[2]    
        listNAXIS[28] = strtemp[1]
        listNAXIS[27] = strtemp[0]
        listNAXIS[26] = ' '
    return  listNAXIS

###写SIMPLE###
listsimple = [' ' for i in range(79)]
listsimple[0:8] = 'SIMPLE  ='
listsimple[29] = 'T'
strsimple = ''.join(listsimple)
encodesimple = strsimple.encode('gbk')
f.write(encodesimple)

###写BITPIX###
listbitpix = [' ' for i in range(79)]
listbitpix[0:8] = 'BITPIX  ='
listbitpix[29] = '2'
listbitpix[28] = '3'
listbitpix[27] = '-'
strbitpix = ''.join(listbitpix)
encodebitpix = strbitpix.encode('gbk')
f.write(encodebitpix)

###写NAXIS###
listNAXIS = [' ' for i in range(79)]
listNAXIS[0:8] = 'NAXIS   ='
listNAXIS[29] = '2'
strNAXIS = ''.join(listNAXIS)
encodeNAXIS = strNAXIS.encode('gbk')
f.write(encodeNAXIS)

###写NAXIS1###
listNAXIS1 = [' ' for i in range(79)]
listNAXIS1 = writeNAXISleng(listNAXIS1,strlie)
listNAXIS1[0:8] = 'NAXIS1  ='
strNAXIS1 = ''.join(listNAXIS1)
encodeNAXIS1 = strNAXIS1.encode('gbk')
f.write(encodeNAXIS1)

###写NAXIS2###
listNAXIS2 = [' ' for i in range(79)]
listNAXIS2 = writeNAXISleng(listNAXIS2,strhang)
listNAXIS2[0:8] = 'NAXIS2  ='
strNAXIS2 = ''.join(listNAXIS2)
encodeNAXIS2 = strNAXIS2.encode('gbk')
f.write(encodeNAXIS2)

###写EXTEND###
listEXTEND = [' ' for i in range(79)]
listEXTEND[0:8] = 'EXTEND  ='
listEXTEND[29] = 'T'
strEXTEND = ''.join(listEXTEND)
encodeEXTEND = strEXTEND.encode('gbk')
f.write(encodeEXTEND)

###写END###
listEND = [' ' for i in range(79)]
listEND[0:2] = 'END'
strEND = ''.join(listEND)
encodeEND = strEND.encode('gbk')
f.write(encodeEND)

###头文件补空格36-7=29###
listkong = [' ' for i in range(80)]
strkong = ''.join(listkong)
encodekong = strkong.encode('gbk')
for j in range(29):
    f.write(encodekong)

###转置变成浮点数存###
data = imageT.astype(np.float32)
for i in range(hang):
    for j in range(lie):
        dbytes = struct.pack('>f',data[i][j]) #低位在前
        f.write(dbytes)
        
###data补空格(hang*lie*4+2880+x)/2880 = n  ###
n = math.ceil((hang*lie*4+2880)/2880)   #根据公式计算
x = n*2880-hang*lie*4-2880
listdkong = [' ' for i in range(x)]
strdkong = ''.join(listdkong)
encodedkong = strdkong.encode('gbk')
f.write(encodedkong)
  
f.close()
