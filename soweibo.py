#coding:utf8

import requests, webbrowser, time
from urllib import quote
import smtplib


def fetchweibos(kword):
	url = 'http://s.weibo.com/weibo/%s&typeall=1&suball=1&timescope=custom:%s-0&Refer=g'
	headers = {'user-agent': \
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/532 (KHTML, like Gecko) Chrome/45 Safari/532 Fck',\
	'Cookie': \
	'SINAGLOBAL=1645489266019.149.1470792372411; SCF=AtZCZIRlC5wiArrVF9MWe7qvnErH-dD5L4oSB-Ep7jFwx9YS5BE0oAOhwkkQFLWS7CSCkqI9QROmvcfU0d5uthU.; SUHB=079ygO35U-w-mV; _s_tentry=login.sina.com.cn; Apache=2908473703816.1836.1477281351697; ULV=1477281351705:107:21:3:2908473703816.1836.1477281351697:1477272550916; SWB=usrmdinst_1; UOR=,,login.sina.com.cn; WBtopGlobal_register_version=96e660181b891f73; NSC_wjq_txfjcp_mjotij=ffffffff094113d345525d5f4f58455e445a4a423660; ULOGIN_IMG=14773020205331; ALF=1479894076; SUB=_2A251CadsDeTxGedJ41US-CfMzjmIHXVW9ckkrDV8PUJbkNAKLXPykW1xh9c7XwWqNxtK9m86_dVc8YfCCw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWDJnyk.zvzlVgr7aS-ogCG5JpX5oz75NHD95QpS0nNe0n4eh-fWs4Dqcj.i--ciKLhi-2Ri--Ni-i8iKyWi--fiK.7iKyhi--fi-82i-2c; WBStorage=86fb700cbf513258|undefined'}
	#add %25
	url = url %(quote(kword).replace('%', "%25"), time.strftime('%Y-%m-%d', time.localtime()))
	html = requests.get(url, headers=headers).content

	cur = 0
	if html.find("noresult_tit") == -1:
		cur = html.count('WB_cardwrap S_bg2 clearfix')
	if html.find("yzm_change") > -1:
		print 'Blocked'
		exit()
	elif cur > kword_dict[kword]:
		kword_dict[kword] = cur
		showmsg(url)
		

def showmsg(msg):
	webbrowser.open_new_tab(msg)

#txt should be utf8 format
def fetchkword():
	for kword in open("kword.txt"):
		kword = kword.strip()
		kword_dict[kword] = 0

kword_dict = {}
fetchkword()
i=0
while True:
	for kword in kword_dict.keys():
		i +=1
		print '%s.%s:Now starting ...' %(i, kword.decode('utf8'))
		fetchweibos(kword)
		time.sleep(15)
	print "==============================="
	time.sleep(30)
