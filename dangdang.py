# coding: utf-8
from bs4 import BeautifulSoup
import os
import urllib
import requests
import re
import json #解析json格式的html
import pandas as pd #用来存储抓取的数据
from pandas import DataFrame,Series

shu = ['493776',
'9206992',
'9053948',
'9206995',
'9053932',
'9274514',
'9274511',
'9274512',
'9274516',
'9274513'
]


header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}


file = "f:/dangdang/zuozhe"
file2 = "f:/dangdang/duanluo"
file3 = "f:/dangdang/neirong"
img_path = 'f:/dangdang/lunbotu'#轮播图存储路径
img_xq = 'f:/dangdang/xiangqingtu'#详情页图存储路径
img_zhaiyao = 'f:/dangdang/zhaiyao'#摘要图存储路径

def makedirs(path):  
		folder = os.path.exists(path)#判断路径下文件夹是否存在
		if not folder:
			os.makedirs(path)#mkdir 和 makedirs
			print ("picture文件夹创建成功") 
		else:  
			print ("picture文件夹已经存在")  

makedirs(file) 
makedirs(file2)
makedirs(file3)
makedirs(img_path)
makedirs(img_xq) 
makedirs(img_zhaiyao) 

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

get_sn_bianma(Referer,header)

#**************************************************************************************************************************************
#Referer = 'http://product.dangdang.com/25310278.html'
list_dongxi = []
def Gethref(Referer,header):#抓取作者
	try:
		html = requests.get(Referer,headers = header)
		soup_first = BeautifulSoup(html.text,'lxml')
		list_dongxi.append('sn编码:'+ get_sn_bianma(Referer,header))#添加sn编码
		list_first = soup_first.find('div',class_='messbox_info')
		soup_1 = list_first.find('span',class_='t1',id="author")
		soup_2 = list_first.find('span',class_='t1',dd_name="出版社")
		soup_3 = list_first.find_all('span',class_='t1')[2]
		soup_4 = list_first.find_all('span',class_='t1')[4]
		list_dongxi.append(soup_1.get_text())#作者简介
		list_dongxi.append(soup_2.get_text())#出版社
		list_dongxi.append(soup_3.get_text())#出版时间
		list_dongxi.append("评论数:"+soup_4.get_text().replace("\n","").replace("\r",""))#评论数
		list_third = soup_first.find('div',class_='pro_content')
		soup_third = list_third.find_all('li')[2]
		list_dongxi.append(soup_third.get_text())#添加装订 
	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		succefull='--------' + i + '作者信息添加成功---------'
		print(succefull)


#**************先添加后导出**************************
#list_dongxi填充作者信息
for i in shu:
	Referer = 'http://product.dangdang.com/'+str(i)+'.html'
	Gethref(Referer,header)#抓取作者

#填充完之后再写入txt
def save_zuozhe():#作者txt存储文字
	try:
		os.getcwd()
		os.chdir(file)
		with open('zuozhe.txt','w',encoding='utf-8') as fo:
			fo.write('\n'.join(list_dongxi))
			fo.close()
	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		succefull='----------作者信息导出成功---------'
		print(succefull)

save_zuozhe()

#将txt文档按要求放入excel中
def save_excel():
	os.getcwd()
	os.chdir('F:/dangdang/第二批/zuozhe2')
	with open('zuozhe.txt',encoding='utf-8') as fn:
	    lines = fn.readlines()
	#txt放入excel里
	js = {}
	jss = []
	for line in lines:
		print(line.strip())
		# print(line.strip())
		(key, value) = line.strip().replace('：', ':').split(':')
		#print ((key, value))
		js[key] = value
		print (js)
		# 解析到“包 装” 说明是一条记录
		if '包 装' == key:
		    jss.append(js)
		    js = {}#清空js
	# 将“js”数据的数组“jss” 转换为 df
	df = pd.DataFrame.from_records(jss)
	#存储到excel
	writer = pd.ExcelWriter('F:/dangdang/第二批/zuozhe2.xlsx')
	try:
		df.to_excel(writer, sheet_name = 'data',encoding='utf-8',index=False,header=0)
		writer.save()
		writer.close()

	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		succefull='导出成功'
		print(succefull)

save_excel()

#*******************************************************************************************************************************

#Referer = 'http://product.dangdang.com/25310278.html'
def Gethref3(Referer,header):#抓取轮播图
	try:
		html = requests.get(Referer,headers = header)
		soup_first = BeautifulSoup(html.text,'lxml')
		list_first = soup_first.find('div',class_='messbox_info')
		s = get_sn_bianma(Referer,header)
		soup_six = BeautifulSoup(html.text,'lxml')
		img = soup_six.find('div',class_="big_pic")
		img = img.find('img')
		shu = img['src'].split('-')
		#print(shu)
		url = shu[0] + '-'+ str(1) + '_u_2.jpg'
		print (url)
		#tu = url.split('/')[-1]
		try:
			urllib.request.urlretrieve(url,'{}/{}.jpg'.format(img_path,get_sn_bianma(Referer,header) +'_'+'b'))#url,路径
			print('正在打印轮播图片'+ s +'_'+'b')
		except Exception as e:
			print (e)
	except Exception as e:
			print (e)
#导出轮播图
for i in shu:
	Referer = 'http://product.dangdang.com/'+str(i)+'.html'
	Gethref3(Referer,header)



#*******************************************************************************************************************************

#抓取详情页
def get_img(img_url,header,Referer):#抓取详情页图片
	web_data = requests.get(img_url, headers=header)
	html = requests.get(Referer,headers = header)
	try:
		soup_first = BeautifulSoup(html.text,'lxml')
		list_third = soup_first.find('div',class_='pro_content')
		soup_four = list_third.find_all('li')[4]
		ret = re.findall(r'\d*',soup_four.get_text())#sn编码
		#print(web_data.encoding)
		web_data.encoding = 'UTF-8'
		#print(web_data.encoding)
		#print(web_data.content)
		data = json.loads(web_data.content)#Json格式字符串解码，转换成Python对象;json.dumps()把一个Python对象编，码转换成Json字符串。
		# print(data['data']['html'])
		soup = BeautifulSoup(data['data']['html'], 'lxml')
		img = soup.find('div',class_="descrip")
		imgurl = img.find('img')['src']
		print (imgurl)
		try:
			urllib.request.urlretrieve(imgurl,'{}/{}.jpg'.format(img_xq,ret[11] +'_'+'c'))#url,路径
			print('已经打印出图片'+ ret[11] +'_'+'c')
		except Exception as e:
			print (e)
	except Exception as e:
		print (e)


for i in shu:
	img_url= 'http://product.dangdang.com/index.php?r=callback%2Fdetail&productId='+str(i)+'&templateType=publish&describeMap=0100003041%3A1&shopId=0&categoryPath=01.41.70.01.01.00'
	Referer = 'http://product.dangdang.com/'+str(i)+'.html'
	get_img(img_url,header,Referer)

#***************************************************************************************************************************************
#Referer = 'http://product.dangdang.com/25342352.html'
#抓取品牌方
for i in shu:
	try:
		list_dongxi2 = []
		Referer = 'http://product.dangdang.com/' + str(i)+'.html'
		html = requests.get(Referer,headers = header)
		soup_five = BeautifulSoup(html.text,'lxml')
		list_four = soup_five.find('div',class_='name_info')
		soup_six = list_four.find('span',class_='head_title_name')
		list_dongxi2.append(soup_six.get_text().strip())
		soup_sever = list_four.find('span',class_='hot')
		list_dongxi2.append(soup_sever.get_text().strip())
		sn.append(get_sn_bianma(Referer,header))
		save_pinpai()
	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		try:
			succefull='**********'+ i + '---' + get_sn_bianma(Referer,header) +'品牌信息导出成功**********'
			print(succefull)
		except Exception as err:
			fillte='导出失败:'+str(err)
			print(fillte)	


def save_pinpai():
	try:
		os.getcwd()
		os.chdir(file2)
		with open(get_sn_bianma(Referer,header)+'_'+'pinpai''.txt','w',encoding='utf-8') as fo:
			fo.write('\n'.join(list_dongxi2))
			fo.close()
	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		succefull='**********'+ i + '---' + get_sn_bianma(Referer,header) +'品牌信息导出成功**********'
		print(succefull)

save_pinpai()



#********************************************************************************************************************************************88

#抓取详情页的内容,放入txt文档,此处保留，但不满足工作要求,有另一版本放入excel的。
for i in shu:
	kuang = []
	img_url= 'http://product.dangdang.com/index.php?r=callback%2Fdetail&productId='+str(i)+'&templateType=publish&describeMap=0100003041%3A1&shopId=0&categoryPath=01.41.70.01.01.00'
	try:
		web_data = requests.get(img_url, headers=header)
		web_data.encoding = 'UTF-8'
		data = json.loads(web_data.content)#Json格式字符串解码，转换成Python对象;json.dumps()把一个Python对象编，码转换成Json字符串。
		#print(data)
		soup = BeautifulSoup(data['data']['html'], 'lxml')
		div = soup.find('div', id="abstract")#拿到编辑推荐
		ds = soup.find('div', class_="title")#拿到标题
		kuang.append(ds.text)
		ps = div.find_all('p')
		for p in ps:
		    kuang.append("".join(p.text.split()))# join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串。

		div1 = soup.find('div', id="content")#拿到内容简介
		ds1 = div1.find('div', class_="title")#拿到标题
		kuang.append(ds1.text)
		ps1 = div1.find_all('p')
		for p in ps1:
		    kuang.append("".join(p.text.split()))

		div2 = soup.find('div', id="authorIntroduction")#拿到作者简介
		ds2 = div2.find('div', class_="title")#拿到标题
		kuang.append(ds2.text)
		ps3 = div2.find_all('p')
		for p in ps3:
		    kuang.append("".join(p.text.split()))

	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		succefull='**********'+ i +'详情页抓取成功**********'
		print(succefull)

	try:
		os.getcwd()
		os.chdir(file3)
		Referer = 'http://product.dangdang.com/' + str(i)+'.html'
		with open(get_sn_bianma(Referer,header)+'_'+'b''.txt','w') as fo:
			fo.write('\n'.join(kuang))
			fo.close()
		kuang = []
	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		succefull='**********详情页内容下载成功**********'
		print(succefull)


#*****************************************************************************************************************************
#抓取摘要图片
def get_img(img_url,header,Referer):#抓取详情页图片
	try:
		imgurl = []
		web_data = requests.get(img_url, headers=header)
		html = requests.get(Referer,headers = header)
		get_sn_bianma(Referer,header)
		web_data.encoding = 'UTF-8'
		data = json.loads(web_data.content)#Json格式字符串解码，转换成Python对象;json.dumps()把一个Python对象编，码转换成Json字符串。
		# print(data['data']['html'])
		soup = BeautifulSoup(data['data']['html'],'lxml')
		#img = soup.find_all('div',class_="descrip")[3]
		img = soup.find_all('div',class_="pic",style="text-align:center")
		for img2 in img:
			tu = img2.find('img')
			imgurl.append(tu)
		for num,s in enumerate(imgurl):
			src = s['data-original']
			urllib.request.urlretrieve(src,'{}/{}.jpg'.format(img_zhaiyao,get_sn_bianma(Referer,header) +'_'+'c'+ '_' + str(num)))#url,路径
			print('已经打印出摘要图片'+ get_sn_bianma(Referer,header) +'_'+'c'+ '_'+ str(num)+ i)
	except Exception as e:
		print (e)

for i in shu:
	img_url= 'http://product.dangdang.com/index.php?r=callback%2Fdetail&productId='+str(i)+'&templateType=publish&describeMap=0100003041%3A1&shopId=0&categoryPath=01.41.70.01.01.00'
	Referer = 'http://product.dangdang.com/'+str(i)+'.html'
	get_img(img_url,header,Referer)