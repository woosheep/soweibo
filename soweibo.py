#coding:utf8

import requests, webbrowser, time
from urllib import quote


global is1st
global curtime

kword_dict = {}

def fetchweibos(kword):
	url = 'http://s.weibo.com/weibo/%s&typeall=1&suball=1&timescope=custom:%s-0&Refer=g'
	headers = {'user-agent': \
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/532 (KHTML, like Gecko) Chrome/45 Safari/532 Fck',\
	'Cookie': \
	'SINAGLOBAL=1645489266019.149.1470792372411; SCF=AtZCZIRlC5wiArrVF9MWe7qvnErH-dD5L4oSB-Ep7jFwx9YS5BE0oAOhwkkQFLWS7CSCkqI9QROmvcfU0d5uthU.; SUHB=079ygO35U-w-mV; UOR=,,login.sina.com.cn; ALF=1479894076; SUB=_2A251CadsDeTxGedJ41US-CfMzjmIHXVW9ckkrDV8PUJbkNAKLXPykW1xh9c7XwWqNxtK9m86_dVc8YfCCw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWDJnyk.zvzlVgr7aS-ogCG5JpX5oz75NHD95QpS0nNe0n4eh-fWs4Dqcj.i--ciKLhi-2Ri--Ni-i8iKyWi--fiK.7iKyhi--fi-82i-2c; wvr=6; SWB=usrmdinst_12; _s_tentry=-; Apache=8448649781523.334.1477528061108; ULV=1477528061137:116:30:12:8448649781523.334.1477528061108:1477439907052; NSC_wjq_txfjcp_mjotij=ffffffff094113d445525d5f4f58455e445a4a423660; ULOGIN_IMG=14775291383503; WBStorage=86fb700cbf513258|undefined'}
	#add %25
	global is1st, curtime
	if (not is1st) and (curtime!=time.strftime('%Y-%m-%d', time.localtime())):
		is1st = True
	curtime =  time.strftime('%Y-%m-%d', time.localtime())
	url = url %(quote(kword).replace('%', "%25"), curtime)
	while True:
		try:
			html = requests.get(url, headers=headers).content
			break
		except Exception, e:
			#skip con err
			print "..X",
			time.sleep(5)
			continue
	return html, url

def checkupd(html, url):
	cur = 0
	if html.find("noresult_tit") == -1:
		cur = html.count('WB_cardwrap S_bg2 clearfix')
	if html.find("yzm_change") > -1:
		print 'Blocked'
		exit()
	news = cur - kword_dict[kword]
	if news >0:
		kword_dict[kword] = cur
		showmsg(url, news)
	else:
		print
		

def showmsg(url, news):
	print 'Got %d' %news
	if not is1st:
		webbrowser.open_new_tab(url)


#txt should be utf8 format
def fetchkword():
	for kword in open("kword.txt"):
		kword = kword.strip()
		kword_dict[kword] = 0


is1st = True
fetchkword()
while True:
	for kword in kword_dict.keys():
		print '%s %s: ' %(time.strftime('%H:%M:%S', time.localtime()), kword.decode('utf8')),
		html,url = fetchweibos(kword)
		print "...",
		checkupd(html, url)
		time.sleep(20)

	is1st = False
	print "==============================="