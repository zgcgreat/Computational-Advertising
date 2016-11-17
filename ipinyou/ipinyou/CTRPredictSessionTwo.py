

import subprocess,time,sys,os,math
from sklearn.metrics import roc_auc_score
from sklearn.metrics import log_loss
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from csv import DictReader









def sigmoid(x):
	#I know it's a common Sigmoid feature, but that's why I probably found
	#it on FastML too: https://github.com/zygmuntz/kaggle-stackoverflow/blob/master/sigmoid_mc.py
    return 1 / (1 + math.exp(-x))














max=[]

def init(length):
    for i in range(length):
        max.append((float)(-9.9))



def insertSort(val):
    j=-1
    for i in range(len(max)):
        if(max[i]<val):
            j=i

        else:
            break

    if(j!=-1):
        for i in range(j):
            if(i!=len(max)-1):
                max[i]=max[i+1]

            max[j]=val


path='/media/mars/Documents/dataset/session2'

lastDay=''
for i in range(1,8):



    if(i<5):
        date='0{0}'.format(i+5)
    else:
        date='{0}'.format(i+5)



    #首次建立并训练模型
    if(i==1):
        cmd='vw {0}/201306{1}/imp.201306{1}.vw -f {0}/201306{1}/model  --ftrl --loss_function logistic'.format(path,date)
        subprocess.call(cmd,shell=True,stdout=subprocess.PIPE)
        lastDay=date
        continue


    #直接训练模型
    cmd='vw {0}/201306{1}/imp.201306{1}.vw -i {0}/201306{2}/model  -f {0}/201306{1}/model  --ftrl --loss_function logistic'.format(path,date,lastDay)
    subprocess.call(cmd,shell=True,stdout=subprocess.PIPE)




    #验证最后一天
    if(i==7):


        length=len(open('{0}/201306{1}/clk.201306{1}.txt'.format(path,date)).readlines())
        init(length)

        cmd='vw {0}/201306{1}/imp.201306{1}.vw -i {0}/201306{2}/model -p {0}/201306{1}/preds.txt --ftrl --loss_function logistic'.format(path,date,lastDay)
        subprocess.call(cmd,shell=True,stdout=subprocess.PIPE)


        with open('{0}/201306{1}/submission.txt'.format(path,date),'w') as outfile:
            outfile.write('Id,Predicted\n')
            for line in open('{0}/201306{1}/preds.txt'.format(path,date)):
                row = line.strip().split(' ')
                pro=sigmoid(float(row[0]))
                insertSort(pro)
                outfile.write('%s,%f\n'%(row[1],pro))

        print(max[0])

        label_reader=DictReader(open('{0}/201306{1}/validation.csv'.format(path,date)))
        predict_reader=DictReader(open('{0}/201306{1}/submission.txt'.format(path,date)))
        y_true=[]
        y_pred=[]
        y_scores=[]
        for t,row in enumerate(label_reader):
            predict=predict_reader.__next__()
            actual=float(row['Label'])
            predicted=float(predict['Predicted'])

            y_true.append(actual)
            y_scores.append(predicted)

            #按照实际点击率分布比例判定点击max[0] ，传统 0.5
            if(predicted>=max[0]):
                y_pred.append(1)
            else:
                y_pred.append(0)

        auc=roc_auc_score(y_true,y_scores)
        accuracy=accuracy_score(y_true,y_pred)
        precision=precision_score(y_true,y_pred)
        recall=recall_score(y_true,y_pred)
        f1=f1_score(y_true,y_pred)
        confusion_matrix=confusion_matrix(y_true,y_pred)
        logloss=log_loss(y_true,y_scores)

        print('Accuracy: {0} Precision: {1} Recall: {2} F1-Measure: {3}\n'.format(accuracy,precision,recall,f1))

        print(confusion_matrix)
        print('logloss: {0} auc: {1}\n'.format(logloss,auc))


    lastDay=date