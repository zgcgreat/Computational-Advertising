from userAgentParser import parseUserAgent

__author__ = 'mars'

data_path=''
save_path=''
output='/media/mars/Documents/dataset/session1/20130311/imp.20130311.vw'
input='/media/mars/Documents/dataset/session1/20130311/imp.20130311.csv'

read = open(input)


#------------ 已废除，不再使用！！！！！！！！！！--------------------------


IMPRESSION_FIELDS=['bid_id','timestamp','type','ipinyou_id','user-agent','ip','region','city','ad_exchange','domain','url','anonymous_url_id','ad_slot_id','ad_slot_width','ad_slot_height','ad_slot_visibility','ad_slot_format','ad_slot_floor_price','creative_id','bidding_price','paying_price','key_page_url']



with open(output,'w') as out:
    for t,line in enumerate(read):
        data=line.split('\t')
        categorical_features=[]
        conjunctive_features=[]

        categorical_features.append('hour={0}'.format(data[IMPRESSION_FIELDS.index('timestamp')][8:10]))
        categorical_features.append('{0}={1}'.format('ipinyou_id',data[IMPRESSION_FIELDS.index('ipinyou_id')]))


        categorical_features.append('{0}={1}'.format('ua',parseUserAgent(data[IMPRESSION_FIELDS.index('user-agent')].strip(' '))))

        categorical_features.append('{0}={1}'.format('ip',data[IMPRESSION_FIELDS.index('ip')]))
        categorical_features.append('{0}={1}'.format('region',data[IMPRESSION_FIELDS.index('region')]))
        categorical_features.append('{0}={1}'.format('city',data[IMPRESSION_FIELDS.index('city')]))
        categorical_features.append('{0}={1}'.format('ad_exchange',data[IMPRESSION_FIELDS.index('ad_exchange')]))
        categorical_features.append('{0}={1}'.format('domain',data[IMPRESSION_FIELDS.index('domain')]))
        categorical_features.append('{0}={1}'.format('url',data[IMPRESSION_FIELDS.index('url')]))
        categorical_features.append('{0}={1}'.format('ad_slot_id',data[IMPRESSION_FIELDS.index('ad_slot_id')]))
        categorical_features.append('{0}={1}'.format('ad_slot_visibility',data[IMPRESSION_FIELDS.index('ad_slot_visibility')]))
        categorical_features.append('{0}={1}'.format('ad_slot_format',data[IMPRESSION_FIELDS.index('ad_slot_format')]))
        categorical_features.append('{0}={1}'.format('creative_id',data[IMPRESSION_FIELDS.index('creative_id')]))
        categorical_features.append('{0}={1}'.format('key_page_url',data[IMPRESSION_FIELDS.index('key_page_url')]))


        conjunctive_features.append('ad_slot_size={0}{1}'.format(data[IMPRESSION_FIELDS.index('ad_slot_width')],data[IMPRESSION_FIELDS.index('ad_slot_height')]))


        if(data[IMPRESSION_FIELDS.index('type')=='1']):
            label=0
        else:
            label=1

        out.write('{0} \'{1} |feats {2} {3}\n'.format(label,data[IMPRESSION_FIELDS.index('bid_id')],' '.join(['{0}'.format(val) for val in categorical_features]).strip('\n'),' '.join(['{0}'.format(val) for val in conjunctive_features]).strip('\n')))









