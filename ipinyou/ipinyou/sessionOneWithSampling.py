# -*- coding: utf-8 -*-
from userAgentParser import parseUserAgent
from utils import enumCounter
import random

__author__ = 'mars'




#day='20130311'
day=sys.arg[1]


output='/media/mars/Documents/dataset/session1/{0}/imp.{0}.vw'.format(day)
imp='/media/mars/Documents/dataset/session1/{0}/imp.{0}.txt'.format(day)
clk='/media/mars/Documents/dataset/session1/{0}/clk.{0}.txt'.format(day)
validation='/media/mars/Documents/dataset/session1/{0}/validation.csv'.format(day)


IMPRESSION_FIELDS=['bid_id','timestamp','type','ipinyou_id','user-agent','ip','region','city','ad_exchange','domain','url','anonymous_url','ad_slot_id','ad_slot_width','ad_slot_height','ad_slot_visibility','ad_slot_format','ad_slot_floor_price','creative_id','bidding_price','paying_price','key_page_url']


'''

#----------初始化属性次数统计器----------
ipinyou_counter=enumCounter('ipinyou_id')
ip_counter=enumCounter('ip')
region_counter=enumCounter('region')
url_counter=enumCounter('url')
adslotid_counter=enumCounter('ad_slot_id')
creativeid_counter=enumCounter('creative_id')
keypageurl_counter=enumCounter('key_page_url')
domain_counter=enumCounter('domain')
ua_counter=enumCounter('useragent')
city_counter=enumCounter('city')
ad_slot_format_counter=enumCounter('ad_slot_format')
adslotsize_counter=enumCounter('adslotsize')
advertiser_id_counter=enumCounter('advertiser_id')
user_tags_counter=enumCounter('user_tags')
#-------------------------------------------
'''


#负采样后达到的点击率
CLICK_RATE=0.256
def getSampleRate():
    click=len(open(clk).readlines())
    total=len(open(imp).readlines())
    click*=0.93
    rate=click*(1-CLICK_RATE)/(total*CLICK_RATE)
    #原始数据中的点击和曝光总数
    print('clicks: {0} impressions: {1}\n'.format(click,total))
    #一个负例被选中的概率，每多少个负例被选中一次
    print('sample rate: {0} sample num: {1}'.format(rate,1/rate))
    return round(1/rate)




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
sample=getSampleRate()


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

        if t%100000==0:
            print('{0} proceed!'.format(t))

        if label==-1:

            #负采样，只有1/sample的概率选择一条负例，未选中直接跳过
            if random.randint(1,sample)!=random.randint(1,sample):
                continue
            valid.write('{0},{1}\n'.format(data[IMPRESSION_FIELDS.index('bid_id')],0))

        out.write('{0} \'{1} |feats {2} {3}\n'.format(label,data[IMPRESSION_FIELDS.index('bid_id')],' '.join(['{0}'.format(val) for val in categorical_features]).strip('\n'),' '.join(['{0}'.format(val) for val in conjunctive_features]).strip('\n')))





#--------------------------------------------------------------------------------

'''

#------------------------------统计各属性的出现次数-------------------------------------------------------------

        ipinyou_counter.count(getVal(data,'ipinyou_id'))
        ip_counter.count(getVal(data,'ip'))
        region_counter.count(getVal(data,'region'))
        url_counter.count(getVal(data,'url'))
        adslotid_counter.count(getVal(data,'ad_slot_id'))
        creativeid_counter.count(getVal(data,'creative_id'))
        keypageurl_counter.count(getVal(data,'key_page_url'))
        domain_counter.count(getVal(data,'domain'))
        ua_counter.count(parseUserAgent(parseUserAgent(getVal(data,'user-agent').strip(' '))))
        city_counter.count(getVal(data,'city'))
        ad_slot_format_counter.count(getVal(data,'ad_slot_format'))
        adslotsize_counter.count('{0}x{1}'.format(data[IMPRESSION_FIELDS.index('ad_slot_width')],data[IMPRESSION_FIELDS.index('ad_slot_height')]))
        advertiser_id_counter.count(getVal(data,'advertiser_id'))

#------------------------------counter-----------------------------------------------------------------
'''


'''
ipinyou_counter.showCount()
ip_counter.showCount()
region_counter.showCount()
url_counter.showCount()
adslotid_counter.showCount()
creativeid_counter.showCount()
keypageurl_counter.showCount()
domain_counter.showCount()
ua_counter.showCount()
city_counter.showCount()
ad_slot_format_counter.showCount()
adslotsize_counter.showCount()

user_tags_counter.showCount()
#user_tags_counter.getDetail()
advertiser_id_counter.showCount()

'''



'''

#------------------------------------------------------验证打标签的数量是否正确

click_counter.getDetail()

act_click=0
act_total=0
for t,line in enumerate(open(output)):
    val=line.split()[0]
    if val=='1':
        act_click+=1

    act_total+=1


print('the vw output, clicks: {0} impressions: {1}, CTR:{2}'.format(act_click,act_total,act_click/act_total))
#------------------------------------------------------


'''