import urllib.request
import json
import pya3rt

def getChat(txt):
	key =''
	client = pya3rt.TalkClient(key)
	reply_message = client.talk(txt)
	print(reply_message['results'][0]['reply'])
	return reply_message['results'][0]['reply']

def getStockInfo():
	#エンドポイントURL
	url = 'https://webapi.yanoshin.jp/webapi/tdnet/list/3382.json?limit=1'
	#リクエストを送っている
	req = urllib.request.Request(url)
	with urllib.request.urlopen(req) as res:

		#レスポンスを読める形にする
		response = res.read().decode("utf-8")
		response = json.loads(response)
		print(response['items'][0]['Tdnet'])
		print(response)
