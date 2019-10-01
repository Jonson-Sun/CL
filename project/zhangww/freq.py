from jieba import cut #分词工具

文件名="张维为"  #数据文件
频率字典={}

def 读文件(name):
	with open(name) as 文件流:
		行表=文件流.readlines()
	return 行表

def cut_freq():
	行表=读文件(文件名)
	for 行 in 行表:
		#print(行)
		词列=[项 for 项 in cut(行)]
		#print(len(词列))
		for 词 in 词列:
			if 词 in 频率字典.keys():
				频率字典[词]+=1
			else:
				频率字典[词]=1
	return 频率字典

def 去冗排序():
	#去掉单个字符的 词
	频率字典=cut_freq()
	待删除表=[]
	for 词 in 频率字典.keys():
		if len(词) ==1:
			待删除表.append(词)
			
	for 词 in 待删除表:
		del 频率字典[词]
		
	print("频率字典大小:",len(频率字典))
	排序表=sorted(频率字典.items(),key=lambda d:d[1],reverse=True)
	print("去冗排序 :\n",排序表[0:100])
	
def 原生排序():
	频率字典=cut_freq()
	print("频率字典大小:",len(频率字典))
	排序表=sorted(频率字典.items(),key=lambda d:d[1],reverse=True)
	print("原生排序:\n",排序表[0:100])
	
#原生排序()
去冗排序()