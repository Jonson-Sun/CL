#!/home/asen/miniconda3/bin/python
from  urllib.request import urlopen
def num2str(num):
	码长=5  # sz,sh 是 6
	tmp=str(num)
	位数=len(tmp)
	if 位数 < 码长:
		tmp='0'*(码长-位数)+tmp
	else:
		tmp=tmp[-码长:]
	return tmp
	
def 获得股票代码1(flag="hk"): #遍历法 : 时间相当长
	count=0
	for num in range(1,100000):
		tmp=num2str(num)
		#print(tmp)
		yield tmp
		if num%10000 == 0 :
			print(count,"万次.")
			count+=1
#获得股票代码()
def 获得股票代码2(flag="sh"): #建立在1之上: sh时间在6s左右
	if flag == "sh" :
		文件="sh_finace.txt"
	elif flag == "sz":
		文件="sz_finace.txt"
	else:
		文件="hk_finace.txt"
	代码表=""
	count=0
	with open(文件,'r') as readfile:
		for line in readfile.readlines():
			if count < 500:  # 100,800 都会速度变慢
				linearray=line.split(',');
				assert(len(linearray[0])==6)
				代码表+=flag+linearray[0]+',' 
				count+=1
			else:
				yield 代码表
				代码表=""
				count=0
	yield 代码表
			
def 下载数据(flag):
	#下载数据到文件
	with open(flag+"data.txt","a") as io:
		for num in 获得股票代码2(flag):
			url="http://hq.sinajs.cn/list="+num
			#url="http://hq.sinajs.cn/list=sz"+num
			f=urlopen(url)
			for str_line in f.readlines():
				str_line=str(str_line,encoding='gbk').split("\"")
				#str_line=str_line[1].split(",")
				#print(str_line)
				if len(str_line[1]) > 10 :
					io.write(str_line[1]+"\n")
				#break
	#print("数据写入完成!")
	return True
def 下载数据2(flag):
	#下载数据到文件
	with open("finace.txt","a") as io:
		for num in 获得股票代码1(flag):
			try:
				url="http://hq.sinajs.cn/list="+flag+num
				#url="http://hq.sinajs.cn/list=sz"+num
				f=urlopen(url)
				str_line = f.readline()
				str_line=str(str_line,encoding="gbk").split("\"")
				#str_line=str_line[1].split(",")
				#print(str_line)
				if len(str_line[1]) > 10 :
					io.write(str_line[1]+"\n")
				#break
			except UnicodeDecodeError:
				print("gbk 编码出错")
				continue
	print("数据写入完成!")
	return True
下载数据("sh") #上交所
下载数据("sz")  #深交所
#下载数据2("hk")


"""
http://hq.sinajs.cn/list=gb_amzn

0：”大秦铁路”，股票名字；2列
1：”27.55″，今日开盘价；3
2：”27.25″，昨日收盘价；4
3：”26.91″，当前价格；5
4：”27.55″，今日最高价；
5：”26.20″，今日最低价；
6：”26.91″，竞买价，即“买一”报价；
7：”26.92″，竞卖价，即“卖一”报价；
8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
10：”4695″，“买一”申请4695股，即47手；
11：”26.91″，“买一”报价；
12：”57590″，“买二”
13：”26.90″，“买二”
14：”14700″，“买三”
15：”26.89″，“买三”
16：”14300″，“买四”
17：”26.88″，“买四”
18：”15100″，“买五”
19：”26.87″，“买五”
20：”3100″，“卖一”申报3100股，即31手；
21：”26.92″，“卖一”报价
(22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四?的情况”
30：”2008-01-11″，日期；
31：”15:05:32″，时间；

"""