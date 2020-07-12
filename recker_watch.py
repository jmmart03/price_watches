import unicodedata
import json
import http.client, urllib
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import datetime

root_url = 'http://www.thecomfortzone.com/appliances/shop'

pushover_token = ''
pushover_user = ''

target_list = [
	{'target_item':'PHS930SLSS','url':'http://www.thecomfortzone.com/appliances/shop/productList.asp?categoryid=30&cl=8,16,'}
	,{'target_item':'GNE29GSKSS','url':'http://www.thecomfortzone.com/appliances/shop/productList.asp?categoryid=33&cl=8,17,'}
]

print(datetime.datetime.now().isoformat())
for target in target_list:
	client = uReq(target.get('url'))
	soup = BeautifulSoup(client.read(), 'html.parser')

	links = []
	#print('target',target.get('target_item'))
	for a in soup.find_all('a'):
		text = a.contents[0]
		if text is not None:
			links.append({'linktext':unicodedata.normalize('NFKD',str(text)),'href':a.get('href')})

	result = next((item for item in links if target.get('target_item') in item["linktext"]), False)
	print(result)
	#if we found the range, send a message
	if result is not False:
		pushover_msg = 'Found '+target.get('target_item')+' at R&B. '+root_url+result.get('href')
		print('sending message',pushover_msg)
		conn = http.client.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
			urllib.parse.urlencode({
			"token": pushover_token,
			"user": pushover_user,
			"message": pushover_msg,
		}), { "Content-type": "application/x-www-form-urlencoded" })
		conn.getresponse()

