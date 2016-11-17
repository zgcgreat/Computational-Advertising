from userAgentParser import parseUserAgent
from utils import enumCounter
__author__ = 'mars'

session='2'
day='20130606'

output='/media/mars/Documents/dataset/session{1}/{0}/imp.{0}.vw'.format(day,session)
imp='/media/mars/Documents/dataset/session{1}/{0}/imp.{0}.txt'.format(day,session)
clk='/media/mars/Documents/dataset/session{1}/{0}/clk.{0}.txt'.format(day,session)
validation='/media/mars/Documents/dataset/session{1}/{0}/validation.csv'.format(day,session)



IMPRESSION_FIELDS=['bid_id','timestamp','type','ipinyou_id','user-agent','ip','region','city','ad_exchange','domain','url','anonymous_url','ad_slot_id','ad_slot_width','ad_slot_height','ad_slot_visibility','ad_slot_format','ad_slot_floor_price','creative_id','bidding_price','paying_price','key_page_url','advertiser_id','user_tags']



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




#--------------------从click日志中找出所有的bid_id，以便给imp数据打标签（是否点击）
click_counter=enumCounter('click')
clk_bid_id=set()





for t,line in enumerate(open(clk)):
    data=line.split('\t')
    clk_bid_id.add(getVal(data,'bid_id'))

valid=open(validation,'w')
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
            label=1
    #        print(getVal(data,'bid_id'))
            click_counter.count('click')

            valid.write('{0},{1}\n'.format(data[IMPRESSION_FIELDS.index('bid_id')],1))
        else:
            label=-1
            valid.write('{0},{1}\n'.format(data[IMPRESSION_FIELDS.index('bid_id')],0))



        out.write('{0} \'{1} |feats {2} {3}\n'.format(label,data[IMPRESSION_FIELDS.index('bid_id')],' '.join(['{0}'.format(val) for val in categorical_features]).strip('\n'),' '.join(['{0}'.format(val) for val in conjunctive_features]).strip('\n')))
        if t%100000==0:
            print('{0} proceed!'.format(t))



