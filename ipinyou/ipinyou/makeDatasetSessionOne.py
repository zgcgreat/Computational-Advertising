# -*- coding: utf-8 -*-

import subprocess,time,sys,os,math





for i in range(1,8):



    #采样

    cmd='python sessionOneWithSampling.py 2013031{0}'.format(i)
    subprocess.call(cmd,shell=True,stdout=subprocess.PIPE)


    print('2013031{0} vw dataset prepared!'.format(i))



