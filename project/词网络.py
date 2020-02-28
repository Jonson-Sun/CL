#! -*- utf8 -*-
'''
	1. 我在那里
	2. [我,在,哪里]
	3. 我--在--哪里

'''

from jieba import cut
from os import system
from re import sub as resub

#全局量
数据列=[];
结果串="";
数据文件名="数据.txt"; 
结果文件名="结果.txt";

# 文件操作
def 读文件到列表(文件名):
	global 数据列;
	with open(文件名,'r') as 文件流:
		数据列=文件流.readlines();
		#数据列=数据[0:100]
	return True;

def 将数据写入文件(串,文件名):
	前缀="graph G { \n";
	后缀="\n }\n ";
	串=前缀+串+后缀;
	with open(文件名,"w") as 写文件流:
		写文件流.write(串);
	return True;


#功能 子函数
def 分词(单句):
	单词列=cut(单句);
	#"--".join(单词列)
	#然后掐头去尾也行
	return 单词列;

def 替换空格为两个连接符号(单句):
	#只替换句子中间的空格
	临时串="";
	标点=" ¡\\1234567890\t!！@#$%^&()_+?？+-*/,.，。：；‘’“”;:\"\'\'\""
	
	#print(标点)
	for 词 in 单句:
		#去掉标点符号
		if 词 in 标点:
			continue;
		if 词 is not '\n':
			临时串+=词+"--";
		else:
			#去掉--
			临时串=临时串.rstrip('-');
			if len(临时串) >3 :
				临时串+='\n';
	return 临时串;

def 去高频词(分词后的句子):
	高频词=["了","道","你","我","的","去","来","在",\
		 "是","他","便","都","那","也",  \
		 "得","又","把","却","这","人"]
	列表=[]
	
	for x in 分词后的句子:
		if x in 高频词:
			continue
		else:
			列表.append(x)
	return 列表

def 中文文本():
	global 结果串;
	读文件到列表(数据文件名);
		
	for 句子 in 数据列:
		tmp=分词(句子);
		tmp=去高频词(tmp); #print(tmp);
		tmp=替换空格为两个连接符号(tmp);#print(tmp);
		结果串=结果串+tmp+'\n';
		
	将数据写入文件(结果串,结果文件名);
	#执行画图命令 dot
	#system("sfdp -Tsvg 结果.txt -o 中文.svg");
	return True;

def 英文文本():
	global 结果串;
	读文件到列表(数据文件名);
	for 句子 in 数据列:
		s=resub(r'[^\w\s]',' ',句子) #空格
		s="--".join(s.split()); #print(s);
		结果串=结果串+s+'\n';	
	将数据写入文件(结果串,结果文件名);
	return True;

def 英文字母_句子():
	global 结果串;
	读文件到列表(数据文件名);
	for 句子 in 数据列:
		s=resub(r'[^\w]','',句子) #空串
		s="--".join([i for i in s])	
		结果串=结果串+s+'\n';	
	将数据写入文件(结果串,结果文件名);
	return True;

def 英文字母_单词():
	global 结果串;
	读文件到列表(数据文件名);
	for 句子 in 数据列:
		s=resub(r'[^\w\s]',' ',句子) 
		for i in s.split():
			tmp="--".join([x for x in i])
			#print(tmp)
			结果串=结果串+tmp+'\n';	
	将数据写入文件(结果串,结果文件名);
	return True;
#===========================================
def 读取已分词文件():
	global 结果文件名;
	global 数据列;
	with open(结果文件名,'r') as 文件流:
		数据列=文件流.readlines();
	return True;

def 过滤数据():
	global 数据列;
	读取已分词文件();
	for line in 数据列:
		yield line.split("--");
		#其他不同形式的文件格式只需更改此处即可
	return True;
	
def 统计文本中前100高频词():
	高频词表=dict();
	键值集合=高频词表.keys()
	for 词行 in 过滤数据():
		for 词 in 词行:
			if 词 in 键值集合:
				高频词表[词]+=1
			else:
				高频词表[词]=1
	print("高频词表的大小为:",len(高频词表))
	序列=sorted(高频词表.items(), key=lambda item:item[1], reverse=True)
	i=0
	while(i<100):
		print(序列[i])
		i+=1
	return True;

#=================================================
def 无向图改有向图():
	输出文件="结果1.txt"
	串=""
	
	读文件到列表(结果文件名);
	for 句子 in 数据列:
		串+=句子.replace("--","->")
	将数据写入文件(串,输出文件)
	return True;


def main():
	中文文本();
	#英文文本();
	#英文字母_句子();
	#英文字母_单词();
	#统计文本中前100高频词();
	无向图改有向图();

main();




