!/usr/bin/python3

#price watch script for the range

import json
import requests
import sqlite3
import http.client, urllib
from datetime import datetime
from bs4 import BeautifulSoup

db_file = 'price_watch.db'
price_threshold = 10000
url = 'https://www.searsoutlet.com/br/idp/188565/1/1/0/10'

pushover_token = ''
pushover_user = ''
items = [{'url':'https://www.searsoutlet.com/br/idp/188565/1/1/0/10','name':'induction_range'}]

for item in items:

        r = requests.get(item.get('url'))
        s = BeautifulSoup(r.text,features="html.parser")
        price_str = s.find_all('div',{'id':'ffmc--0'})[0].find_all('div',{'class':'plp--price'})[0].find('strong').text
        print(item.get('name'),price_str)

        price = float(price_str.strip().strip('$').replace(',',''))

        #write price into sqlite
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        sql = "insert into price_watch (ts, item, amount) values (DATETIME('now'),?,?);"
        cur.execute(sql,(item.get('name'),price))
        conn.commit()
        conn.close()

        if price < price_threshold:
                #fire pushover alert
                pushover_msg = item.get('name')+' is now cheap! Only '+price_str+'. Go get it.\n'+url
                conn = http.client.HTTPSConnection("api.pushover.net:443")
                conn.request("POST", "/1/messages.json",
                urllib.parse.urlencode({
                "token": pushover_token,
                "user": pushover_user,
                "message": pushover_msg,
                }), { "Content-type": "application/x-www-form-urlencoded" })
                conn.getresponse()
