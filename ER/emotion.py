#！ -*- utf8 -*-
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from jieba import cut
from word2vec import load as wload
from pickle import load,dump
import numpy as np
import random
random.seed(1243)

from keras.models import Model
from keras.models import load_model
from keras.utils import to_categorical
from keras.layers import Dense,Flatten,Input
from keras.layers import Activation,Dropout
from keras.layers.recurrent  import LSTM
from keras.layers.recurrent  import GRU
from keras.layers.merge import concatenate as concat
from sklearn.metrics import classification_report,confusion_matrix

VECTOR_FILE='rtdata/vec_corpus.bin'
TRAIN_FILE='hotel_corpus/hotel_train.txt'
TEST_FILE='hotel_corpus/hotel_test.txt'
PICKLE_FILE='rtdata/tdt40.bin'
EMOTION_MODEL='model/emotion.h5'
LENGTH=30


def sentence_deal(file_name):
	#1、提取情感标签 
	#2、去掉属性，评价。标记 
	#3、分词
	with open(file_name,'r') as f:
		text=f.readlines()
	sentence_list=[]
	label_list=[]
	for line in text:
		tmp=line.split(' ')[1:]
		tmp1=[]
		for words in tmp:
			if words.startswith('[a]'):   #语法错误，缺少冒号。
				words=words[3:]
				tmp1.extend(list(cut(words) ) )
			elif words[0:3]=='[e]':
				words=words[3:]
				tmp1.extend(list(cut(words) ) )
			elif words[0:3]=='[p]':
				label_list.append(words[3])
				#tmp.remove(words)  #直接tmp回收
			else:
				tmp1.append(words)
		sentence_list.append(tmp1)
	#print(sentence_list[0:3])
	#print(label_list[0:10])
	return sentence_list,label_list

def text2vec(sentence_list,label_list):
	#词序列转向量，array化。label array化
	w2v=wload(VECTOR_FILE)
	gvec=w2v.get_vector
	wordtable=w2v.vocab
	rand=random.random
	num_val=[]
	
	for sentence in sentence_list:
		tmp=[]
		count=0
		for words in sentence:
			if count>=LENGTH:
				break
			if words in wordtable:
				tmp.append(gvec(words))
			else:
				tmp.append([rand() for _ in range(100)] )
			count+=1
		if count < LENGTH:
			for _ in range(LENGTH - count):
				tmp.append([0.0 for _ in range(100)])
		assert(len(tmp) == LENGTH )
		num_val.append(tmp)
	#print('np类型数据检测',num_val[12])
	
	return np.asarray(num_val),np.asarray(label_list)

def presist(pickle_obj):
	#数据持久化
	with open(PICKLE_FILE,'wb') as f:
			for obj in pickle_obj:
				dump(obj,f)

#*****************数据预处理完成**************************
def build_model():
	#两层宽的网络也可以达到87.3%
	act='relu'
	start=Input(shape=(30,100) )
	x=LSTM(300,activation=act,return_sequences=True )(start)
	x1=Dropout(0.2)(x)  #88.9=20  89.46=30
	
	x=LSTM(200,activation=act,return_sequences=True )(x1)
	x2=Dropout(0.2)(x) #89.29
	
	x=Dense(10,activation=act )(x2)
	x3=Dropout(0.2)(x)
	
	x=Dense(8,activation=act )(x3)
	x4=Dropout(0.2)(x)
	
	x=Dense(4,activation=act )(x4)
	x=Dropout(0.2)(x) #89.55
	
	#x=concat([x1,x2,x3,x4,x])
	x=Flatten()(x2)
	end=Dense(2,activation='softmax')(x)
	model_D=Model(inputs=start,output=end)
	model_D.summary()
	return model_D  
	
def build_model1():
	act='relu'
	start=Input(shape=(30,100) )
	x=Dense(100,activation=act )(start)
	x=Dropout(0.2)(x)
	x=Dense(80,activation=act )(x)
	x=Dropout(0.2)(x)
	x=Dense(60,activation=act )(x)
	x=Dropout(0.2)(x)
	x=Dense(40,activation=act )(x)
	x=Dropout(0.2)(x)
	x=Dense(20,activation=act )(x)
	x=Dropout(0.2)(x)
	x=Dense(10,activation=act )(x)
	x=Dropout(0.2)(x)
	x=Dense(10,activation=act )(x)
	x=Dense(8,activation=act )(x)
	x=Dense(4,activation=act )(x)
	x=Flatten()(x)
	end=Dense(2,activation='softmax')(x)
	model_D=Model(inputs=start,output=end)
	return model_D  #100 epoch 89.23.5



def main(first_run=False):
	if first_run is True:
		file_all=(TRAIN_FILE,TEST_FILE)
		pickle_obj=[]
		for file_name in file_all:
			sl,ll=sentence_deal(file_name)
			sla,lla=text2vec(sl,ll)
			_size=len(sla)
			input_d=sla.reshape(_size,LENGTH,100)
			output_d=to_categorical(lla[0:_size],2)
			pickle_obj.append(input_d)
			pickle_obj.append(output_d )
		presist(pickle_obj)
	else:
		with open(PICKLE_FILE,'rb') as f:
				train_in=load(f)
				train_out=load(f)
				test_in=load(f)
				test_out=load(f)
		
		emotion_model= build_model()
		emotion_model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy','recall'])
		emotion_model.fit(train_in,train_out, epochs=100, batch_size=128,verbose=2,
				validation_split=0.2
				 )
		emotion_model.save(EMOTION_MODEL)
		#emotion_model.summary()
		
		#进入测试阶段
		model=load_model(EMOTION_MODEL)
		yp = model.predict(test_in, batch_size=128, verbose=2)
		ypreds = np.argmax(yp, axis=1)
		ytrues=np.argmax(test_out,axis=1)
		print('当前模型是:',EMOTION_MODEL)
		targetnames = ['好评', '差评']
		print('多分类报告:')
		print(classification_report(ytrues, ypreds, target_names=targetnames,digits=5))
		print('混淆矩阵:')
		con_mat=confusion_matrix(ytrues, ypreds)   #混淆矩阵:行为真实类别,列为预测类别
		print(con_mat)
		

main()

#500 400 200 100 80 40 20 output_lay
#20轮就可以达到87%的F值  64 32 16 8 2 
#50轮 89 F值


