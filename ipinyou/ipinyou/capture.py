# -*- coding: utf-8 -*-
__author__ = 'mars'

import os, sys



num=100000
output='/media/mars/Documents/dataset/session1/20130311/imp.20130311.csv'



count=0;


#----------截取原始数据，测试用！--------------------

with open(output,'w') as file:
    for line in open('/media/mars/Documents/dataset/session1/20130311/imp.20130311.txt','r'):
        if(count%10000==0):print(count,' processed!')
        file.write(line)
        if(count>=num):
            file.close()
            break
        count+=1

print('dataSet prepared!')