# coding: utf-8
from bs4 import BeautifulSoup
import os
import urllib
import requests
import re
import json
import pandas as pd
from pandas import DataFrame,Series
import xlsxwriter

shu = [
'24143741',
'23617722',
'23192842',
'23965654',
'23711974',
'23711975',
'23711976',
'25299672',
'23940063',
'23999613',
'22617140',
'23268441'
]

header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}

file = "F:/dangdang/第一批/pinpai"

def makedirs(path):  
		folder = os.path.exists(path)#判断路径下文件夹是否存在
		if not folder:
			os.makedirs(path)#mkdir 和 makedirs
			print ("picture文件夹创建成功") 
		else:  
			print ("picture文件夹已经存在")  

def run_makedirs():
	makedirs(file) 

run_makedirs()

def get_sn_bianma(Referer,header):#抓取sn编码
	try:
		html = requests.get(Referer,headers = header)
		soup_first = BeautifulSoup(html.text,'lxml')
		list_third = soup_first.find('div',class_='pro_content')
		soup_four = list_third.find_all('li')[4]
		ret = re.findall(r'\d*',soup_four.get_text())#编码
		return ret[11]
		#ret_list.append(ret[11])
	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		succefull='--------sn编码：打印成功---------'
		print(succefull)

#抓取品牌方
sn2 = []
sn3 = ['sn编码','品牌内容']
sn2.append(sn3)
def run_pinpai():
	try:
		sn = []
		sn.append(get_sn_bianma(Referer,header))
		html = requests.get(Referer,headers = header)
		soup_five = BeautifulSoup(html.text,'lxml')
		list_four = soup_five.find('div',class_='name_info')
		soup_six = list_four.find('span',class_='head_title_name')
		sn.append(soup_six.get_text().strip())
		soup_sever = list_four.find('span',class_='hot')
		sn.append(soup_sever.get_text().strip())
		sn2.append(sn)
	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		try:
			succefull='**********'+ i + '---' + get_sn_bianma(Referer,header) +'品牌信息添加成功**********'
			print(succefull)
		except Exception as err:
			fillte='导出失败:'+str(err)
			print(fillte)	


for i in shu:
	Referer = 'http://product.dangdang.com/'+str(i)+'.html'
	try:
		run_pinpai()
	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		succefull='**********'+'链接有效'+'**********'
		print(succefull)

def to_save():
	try:
		os.getcwd()
		os.chdir("F:/dangdang/第一批/pinpai")
		workbook = xlsxwriter.Workbook('品牌.xlsx')#新建excel
		worksheet = workbook.add_worksheet()#新建sheet
		for j in range(0, len(sn2)):
			worksheet.write_row('A' + str(j + 1), sn2[j])
		workbook.close()
	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		succefull='**********'+'品牌内容导出成功**********'
		print(succefull)

to_save()