#！ -*- utf8 -*-
'''
	可用的意见解释识别系统
		1、首先使用文本读取，进一步可改为命令行窗口输入，进而可以做成GUI输入
			对输入方式进行抽象化
		2、输出先使用 cli方式。
		3、保持模型处理部分保持不变。
		
		
'''
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import numpy as np
from keras.models import load_model
from word2vec import load as wload
from jieba import cut
import random
random.seed(1234)

VECTOR_FILE='rtdata/vec_corpus.bin'
MODEL_FILE='model/GRU_92.6.h5'
LENGTH=30

def rand_data():
	#100 dimention random vector
	tmp=[]
	for _ in range(100):
		tmp.append(random.random() )   #2018-4-29:随机初始化变为0.0初始化
	return tmp


def from_anywhere_import_data():
	#本函数用于多种不同方式的数据导入
	#返回值 ：多行文本对象
	
	#方式1：从文件中读取
	textfile='wait2deal.txt'
	with open(textfile,'r',encoding='utf-8') as f:
		text=f.readlines()
	'''
	#方式2：交互式操作
	text=input('请输入一个意见句：')
	text=text.split('。')
	'''
	return text

def read_input():
	#读取输入: 纯文本,进行分词，向量化，numpy.array格式化,[暂不进行持久化操作]
	#返回：数值矩阵
	text=[]
	num_val=[]
	
	multi_line_text=from_anywhere_import_data()
	for sentence in multi_line_text:
		tmp=list( cut(sentence) )
		text.append(tmp)
		print(tmp)
	
	w2v=wload(VECTOR_FILE)
	gvec=w2v.get_vector
	wordtable=w2v.vocab
	for sentence in text:
		tmp=[]
		count=0
		
		for words in sentence:
			if count>=LENGTH:
				break
			if words in wordtable:
				tmp.append(gvec(words))
			else:
				tmp.append(rand_data() )
			count+=1
		
		if count < LENGTH:
			for _ in range(LENGTH - count):
				tmp.append([0.0 for _ in range(100)])
		assert(len(tmp) == LENGTH )
		num_val.append(tmp)
	
	return np.asarray(num_val)


def model_load(input_data):
	#载入模型进行分类
	
	model=load_model(MODEL_FILE)
	#model.summary()
	
	tmp_preds = model.predict(input_data, verbose=2)
	model_output = np.argmax(tmp_preds, axis=1)
	
	return model_output
	

def result_output(model_output):
	#输出分类结果
	ClassLabel = ('原因', '细节', '建议','条件')
	for result in model_output:
		print('该意见句中包含',ClassLabel[result],'信息。',result)
	





def main():
	'''  数据处理流程控制。 '''
	data_tmp=read_input()
	result_tmp=model_load(data_tmp)
	result_output(result_tmp)


if __name__ =='__main__':
	''' 主函数文档'''
	main()
	print('主函数执行结束。')
