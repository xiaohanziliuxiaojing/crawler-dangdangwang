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

shu = ['493776',
'9206992',
'9053948',
'9206995',
]


header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
#Referer = 'f:/dangdang/xiangqing_neirong'
file = "F:/dangdang/第一批/neirong"
def makedirs(path):  
		folder = os.path.exists(path)#判断路径下文件夹是否存在
		if not folder:
			os.makedirs(path)#mkdir 和 makedirs
			print ("picture文件夹创建成功") 
		else:  
			print ("picture文件夹已经存在")  

makedirs(file) 

#************************************************************************************************************************************
#ret_list = []
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

#抓取详情页的内容
dataes = []
analyse = ['sn编号', '产品特色', '内容简介', '作者简介']
dataes.append(analyse)
def run_xiangqingye_neirong():
	try:
		sentences = []#添加段落
		sentences.append(get_sn_bianma(Referer, header))
		web_data = requests.get(img_url, headers=header)
		web_data.encoding = 'UTF-8'
		data = json.loads(web_data.content)#Json格式字符串解码，转换成Python对象;json.dumps()把一个Python对象编，码转换成Json字符串。
		soup = BeautifulSoup(data['data']['html'], 'lxml')
		div = soup.find('div', id="abstract")#拿到编辑推荐
		ds = soup.find('div', class_="title")#拿到标题

		ps = div.find_all('p')
		txt1 = ''
		txt2 = ''
		txt3 = ''
		for p in ps:
		    txt1 += p.text
		sentences.append(txt1)
		#print(txt1)
		div1 = soup.find('div', id="content")#拿到内容简介
		ds1 = div1.find('div', class_="title")#拿到标题

		#print(ds1.text)
		ps1 = div1.find_all('p')
		for p in ps1:
			 txt2 += p.text
		sentences.append(txt2)
		div2 = soup.find('div', id="authorIntroduction")#拿到作者简介
		ds2 = div2.find('div', class_="title")#拿到标题

		print (analyse)
		ps3 = div2.find_all('p')
		for p in ps3:
			txt3 += p.text
		sentences.append(txt3)
		#print(txt3)
		#print(sentences)
		dataes.append(sentences)
		#print(dataes)

	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		succefull='**********'+ i + '---' + get_sn_bianma(Referer,header) +'详情页内容导出成功**********'
		print(succefull)

for i in shu:
	img_url= 'http://product.dangdang.com/index.php?r=callback%2Fdetail&productId='+str(i)+'&templateType=publish&describeMap=0100003041%3A1&shopId=0&categoryPath=01.41.70.01.01.00'
	Referer = 'http://product.dangdang.com/'+str(i)+'.html'
	try:
		run_xiangqingye_neirong()
	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		succefull='**********'+'链接有效'+'**********'
		print(succefull)

def to_save():
	try:
		os.getcwd()
		os.chdir("F:/dangdang/第一批/neirong")
		workbook = xlsxwriter.Workbook('详情页内容.xlsx')#新建excel
		worksheet = workbook.add_worksheet()#新建sheet
		for j in range(0, len(dataes)):
			worksheet.write_row('A' + str(j + 1), dataes[j])
		workbook.close()
	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		succefull='**********'+'详情页内容导出成功**********'
		print(succefull)

to_save()


