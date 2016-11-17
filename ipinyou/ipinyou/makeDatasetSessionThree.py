

import subprocess,time,sys,os,math



date=''
for i in range(1,8):

    if(i<5):
        date='0{0}'.format(i+18)
    else:
        date='{0}'.format(i+18)

    #采样

    cmd='python sessionTwoThreePositiveWeighting.py 3 201310{0}'.format(date)
    subprocess.call(cmd,shell=True,stdout=subprocess.PIPE)


    print('201310{0} vw dataset prepared!'.format(date))



