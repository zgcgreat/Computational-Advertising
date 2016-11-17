from userAgentParser import parseUserAgent
from utils import enumCounter
import sys
__author__ = 'mars'




if len(sys.argv) != 2:
    print('wrong arguments in batch_experiments.py')
    exit(1)


day=sys.argv[1]




output='/media/mars/Documents/dataset/session1/{0}/imp.{0}.vw'.format(day)
imp='/media/mars/Documents/dataset/session1/{0}/imp.{0}.txt'.format(day)
clk='/media/mars/Documents/dataset/session1/{0}/clk.{0}.txt'.format(day)
validation='/media/mars/Documents/dataset/session1/{0}/validation.csv'.format(day)


IMPRESSION_FIELDS=['bid_id','timestamp','type','ipinyou_id','user-agent','ip','region','city','ad_exchange','domain','url','anonymous_url','ad_slot_id','ad_slot_width','ad_slot_height','ad_slot_visibility','ad_slot_format','ad_slot_floor_price','creative_id','bidding_price','paying_price','key_page_url']





def getPositiveWeight():
    click=len(open(clk).readlines())
    total=len(open(imp).readlines())

    print('clicks: {0} impressions: {1}\n'.format(click,total))
    #一个负例被选中的概率，每多少个负例被选中一次
    print('positive weight: {0}'.format(float(total)/click))
    return float(total)/click




#-----------------从一条记录中取出相应属性的属性值-----------------
def getVal(data,name):
    val=data[IMPRESSION_FIELDS.index(name)]
    if val!='null' and val!='' and val!='Na':
        return '{0}={1}'.format(name,val)
    else:
        return ''


#-----------------截取这条记录的时间-----------------
def getTime(data):
    val=data[IMPRESSION_FIELDS.index('timestamp')][8:10]
    if val!='':
        return 'hour{0}'.format(val)

#计算采样率



#--------------------从click日志中找出所有的bid_id，以便给imp数据打标签（是否点击）
click_counter=enumCounter('click')
clk_bid_id=set()


for t,line in enumerate(open(clk)):
    data=line.split('\t')
    clk_bid_id.add(getVal(data,'bid_id'))


#--------------------------------------------------------------------------------









#-----------------读取imp日志，处理成vw格式，并打点击标签，并输出验证集-------
valid=open(validation,'w')
valid.write('Id,Label\n')



PosWgt=getPositiveWeight()
print(PosWgt)
with open(output,'w') as out:
    for t,line in enumerate(open(imp)):

        data=line.split('\t')
        categorical_features=[]
        conjunctive_features=[]

        categorical_features.append(getTime(data))

        categorical_features.append('{0}={1}'.format('ua',parseUserAgent(getVal(data,'user-agent').strip(' '))))
        categorical_features.append(getVal(data,'region'))
        categorical_features.append(getVal(data,'city'))
        categorical_features.append(getVal(data,'ad_exchange'))
        categorical_features.append(getVal(data,'domain'))
        categorical_features.append(getVal(data,'ad_slot_id'))
        categorical_features.append(getVal(data,'ad_slot_visibility'))
        categorical_features.append(getVal(data,'ad_slot_format'))
        categorical_features.append(getVal(data,'creative_id'))
        categorical_features.append(getVal(data,'key_page_url'))


        conjunctive_features.append('{0}{1}'.format(getVal(data,'ad_slot_width'),getVal(data,'ad_slot_height')))


        if(getVal(data,'bid_id') in clk_bid_id):

            click_counter.count('click')
            valid.write('{0},{1}\n'.format(data[IMPRESSION_FIELDS.index('bid_id')],1))
            out.write('1 {0} \'{1}|feats {2} {3}\n'.format(PosWgt,data[IMPRESSION_FIELDS.index('bid_id')],' '.join(['{0}'.format(val) for val in categorical_features]).strip('\n'),' '.join(['{0}'.format(val) for val in conjunctive_features]).strip('\n')))
        else:


            valid.write('{0},{1}\n'.format(data[IMPRESSION_FIELDS.index('bid_id')],0))
            out.write('-1 1.0 \'{0}|feats {1} {2}\n'.format(data[IMPRESSION_FIELDS.index('bid_id')],' '.join(['{0}'.format(val) for val in categorical_features]).strip('\n'),' '.join(['{0}'.format(val) for val in conjunctive_features]).strip('\n')))


        if t%50000==0:
            print('{0} proceed!'.format(t))







#--------------------------------------------------------------------------------
