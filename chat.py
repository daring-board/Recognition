import urllib.request
import json
import pya3rt
import subprocess
from subprocess import Popen

def getChat(filename):
	path = 'speaker/txt/'
	src = path+filename+'.txt'
	dst = path+'dist.txt'
	cmd = 'mecab %s -o %s'%(src, dst)
	proc = Popen(cmd)
	proc.wait()
	lines = [line.strip() for line in open(dst, 'r', encoding='sjis')]
	line = '\n'.join(lines)
	return line

def getChatWithA3rt(txt):
	key ='GRSpAwn90yClWzDvlfG4sWMxzwWcR16r'
	client = pya3rt.TalkClient(key)
	reply_message = client.talk(txt)
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

if __name__=='__main__':
	getChat('あなたの干支')
	getChat('疲れた')
	getChat('こんばんは')
	getChat('眠い')
