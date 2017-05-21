import json
import csv
from urllib.request import urlopen
from urllib.parse import urlencode


api_list=[]

dates=['2014-01-01to2014-01-31','2014-02-01to2014-02-28','2014-03-01to2014-03-31', '2014-04-01to2014-04-30', '2014-05-01to2014-05-30', '2014-06-01to2014-06-30', '2014-07-01to2014-07-31', '2014-08-01to2014-08-31', '2014-09-01to2014-09-30','2014-10-01to2014-10-31','2014-11-01to2014-11-30','2014-12-01to2014-12-31',
'2015-01-01to2015-01-31','2015-02-01to2015-02-28','2015-03-01to2015-03-31', '2015-04-01to2015-04-30', '2015-05-01to2015-05-30', '2015-06-01to2015-06-30', '2015-07-01to2015-07-31', '2015-08-01to2015-08-31', '2015-09-01to2015-09-30','2015-10-01to2015-10-31','2015-11-01to2015-11-30','2015-12-01to2015-12-31',
'2016-01-01to2016-01-31','2016-02-01to2016-02-28','2016-03-01to2016-03-31', '2016-04-01to2016-04-30', '2016-05-01to2016-05-30', '2016-06-01to2016-06-30', '2016-07-01to2016-07-31', '2016-08-01to2016-08-31', '2016-09-01to2016-09-30','2016-10-01to2016-10-31','2016-11-01to2016-11-30','2016-12-01to2016-12-31']

for date in dates:
    d = {'filter': 'all',
         'v': '2',
         'range': date}
    if d not in api_list:
        api_list.append(d)

bloop=[]
for api in api_list:
    bloop.append(json.loads(urlopen('https://events.umich.edu/list/json?'+urlencode(api)).read()))

events = []
for month in bloop:
    for event in month:
        try:
            event = {'startdate':event['date_start'], 'enddate':event['date_end'], 'timestart':event['time_start'], 'timeend':event['time_end'],'title':event['event_title'], 'description':event['description'], 'tags':event['tags'][0]}
            events.append(event)
        except:
            event = {'startdate':event['date_start'], 'enddate':event['date_end'], 'timestart':event['time_start'], 'timeend':event['time_end'],'title':event['event_title'], 'description':event['description'], 'tags':'other'}
            events.append(event)

with open('michigan_events.csv', 'w') as csvfile:
    fieldnames=['title','description','startdate','enddate','timestart','timeend','tags']
    writer= csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for event in events:
        writer.writerow(event)
