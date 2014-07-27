import os,re
import urllib
import sys
import json

cfEmail = 'kfouwels@outlook.com'                        #Login Email Address
cfAPIkey = '7b84202468d22ddf00480e5d015c9a72ca97a'      #API Key, from https://www.cloudflare.com/my-account
domainBase = 'google.com'                               #Domain Name
domainSub = 'google.com'                                #Subdomain to update, full domainBase for root
recordType = 'A'                                        #Domain Type

recordID = 0;                                           #Optional, use to override

if recordID == 0: #Get record ID if not overridden
        data = {'a': 'rec_load_all','tkn': cfAPIkey,'email': cfEmail,'z': domainBase}
        data = urllib.urlencode(data)
        recloadResponse = urllib.urlopen('https://www.cloudflare.com/api_json.html', data).read()
        recloadObj = json.loads(recloadResponse)
        
        if recloadResponse.find(':"error"') == -1 :
                records = recloadObj['response']['recs']['objs']
                for record in records:
                        if record['display_name'] == domainSub:
                                recordID = record['rec_id']
                                break
        else:
                print 'Error'

if recordID != 0:
        print 'recordID', recordID

        f = urllib.urlopen('http://ip-api.com/xml')
        ipe = f.read()
        ip = ipe[ipe.find('<query><![CDATA[')+16:ipe.rfind(']]>',ipe.find('<query><![CDATA['))].strip()
        print 'IP Address:', ip

        data = {
                'a': 'rec_edit',
                'tkn': cfAPIkey,
                'id': recordID,
                'email': cfEmail,
                'z': domainBase,
                'type': recordType,
                'name': domainSub,
                'content': ip,
                'service_mode': '0',
                'ttl': '1'
                }
        data = urllib.urlencode(data)
        update = urllib.urlopen('https://www.cloudflare.com/api_json.html', data)
        response = update.read()
        print 'Update Response:' , response.find('result":')+9
