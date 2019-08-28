# coding: utf-8
from bs4 import BeautifulSoup
import os
import urllib
import requests
import re
import json
import pandas as pd
from pandas import DataFrame,Series

i = '25342352'
Referer = 'http://product.dangdang.com/'+str(i)+'.html'
header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}


def makedirs(path):  
		folder = os.path.exists(path)#判断路径下文件夹是否存在
		if not folder:
			os.makedirs(path)#mkdir 和 makedirs
			print ("picture文件夹创建成功") 
		else:  
			print ("picture文件夹已经存在")  

ret_list = []
list_dongxi = []
def Gethref(Referer,header):#抓取作者
	html = requests.get(Referer,headers = header)
	soup_first = BeautifulSoup(html.text,'lxml')
	list_first = soup_first.find('div',class_='messbox_info')
	soup_second = list_first.find_all('span',class_='t1')#findall返回列表
	for i in soup_second:
		soup_third = BeautifulSoup(i.prettify(),'lxml')
		a = soup_third.get_text().replace('\n','')
		list_dongxi.append(a)
	list_third = soup_first.find('div',class_='pro_content')
	soup_third = list_third.find('ul',class_='key clearfix')
	soup_third = list_third.find_all('li')[2]
	soup_four = list_third.find_all('li')[4]
	ret = re.findall(r'\d*',soup_four.get_text())#编码
	ret_list.append(ret[11])
	list_dongxi.append(soup_third.get_text())  




def Gethref2(Referer,header):#抓取品牌方
	html = requests.get(Referer,headers = header)
	soup_five = BeautifulSoup(html.text,'lxml')
	list_four = soup_five.find('div',class_='name_info')
	soup_six = list_four.find('span',class_='head_title_name')
	list_dongxi.append(soup_six.get_text().strip())
	soup_sever = list_four.find('span',class_='hot')
	list_dongxi.append(soup_sever.get_text().strip())




def Gethref3(Referer,header):#抓取轮播图
	html = requests.get(Referer,headers = header)
	soup_six = BeautifulSoup(html.text,'lxml')
	img = soup_six.find('div',class_="pic")
	img = img.find('img',id="largePic")
	shu = img['src'].split('-')
	for i in range(1,10):
		url = shu[0] + '-'+ str(i) + '_w_10.jpg'
		print (url)
		#tu = url.split('/')[-1]
		try:
			for s in ret_list:
				urllib.request.urlretrieve(url,'{}/{}.jpg'.format(img_path,s+'_'+'b'+'_'+str(i)))#url,路径
				print('正在打印图片'+ s+'_'+'c'+'_'+str(i))
		except Exception as e:
			print (e)


img_url = "http://product.dangdang.com/index.php?r=callback%2Fdetail&productId=24105846&templateType=publish&describeMap=0100003041%3A1&shopId=0&categoryPath=01.41.70.02.03.00"

def get_img(img_url,header):#抓取详情页图片
	web_data = requests.get(img_url, headers=header)
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
		for s in ret_list:
			urllib.request.urlretrieve(imgurl,'{}/{}.jpg'.format(img_xq,s +'_'+'c'))#url,路径
			print('正在打印图片'+ s+'_'+'c')
	except Exception as e:
		print (e)


kuang = []
def get_content(url,header):#抓取详情页里的文字
	web_data = requests.get(url, headers=header)
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



def save():#txt存储文字
	try:
		os.getcwd()
		os.chdir(file)
		for i in ret_list:
			with open(i+'_'+'b''.txt','w') as fo:
				fo.write('\n'.join(list_dongxi))
				fo.write('\n')
				fo.write('\n'.join(kuang))
				fo.close()
	except Exception as err:
		fillte='导出失败:'+str(err)
		print(fillte)
	else:
		succefull='导出成功'
		print(succefull)



file = "f:/dangdang/"
img_path = 'f:/dangdang/lunbotu'#轮播图存储路径
img_xq = 'f:/dangdang/xiangqingtu'#详情页图存储路径


def main():
	makedirs(file) 
	makedirs(img_path)
	makedirs(img_xq) 
	Gethref(Referer,header)
	Gethref2(Referer,header)
	Gethref3(Referer,header)
	get_img(img_url,header)
	get_content(img_url,header)
	save()

if __name__ == "__main__":
	main()

#存储到excel
# for i in ret_list:
# 	writer = pd.ExcelWriter('f:/' + i + '.xlsx')
# 	try:
# 		DataFrame(list_dongxi).to_excel(writer, sheet_name = 'sheet',index=None,header=0)
# 		writer.save()
# 		writer.close()

# 	except Exception as err:
# 		fillte='导出失败:'+str(err)
# 		print(fillte)
# 	else:
# 		succefull='导出成功'
# 		print(succefull)	