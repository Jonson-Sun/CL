#
#保险行业语料/按问题类别选择答案/没有使用神经网络的方法计算句子相关性



#demo ：保险主题 单轮对话
#	1、使用valud.txt进行开发。【量小】
#	2、神经网络模型进行 保险类别 分类，【明白要解决哪一类问题】
#	3、然后可以进一步的问题细分。像保险金额、办理方式、在哪办etc 【明白 问的是问题的哪一方面】
#	4、组织回答：问题类别【如 医疗保险】+具体方面【如；赔偿金额】+结果【数据库查找：3万】
#	

train_file="train.txt"
valid_file='valid.txt'
test_file='test.txt'

allclass=set()
vector_file='vec_corpus.bin'
pickle_file='pick_demo.bin'
LENGTH=40
map_num2class=dict()


import warnings as wn
wn.simplefilter("ignore")

from jieba import cut
from word2vec import load as wload
import numpy as np
from random import random as rand
from pickle import load,dump
from keras.layers import Dense,Activation, Dropout,Flatten,Input
from keras.utils import to_categorical
from keras.models import Model,load_model
from sklearn.metrics import classification_report,confusion_matrix



def rand_data():
	#100 dimention random vector
	tmp=[]
	for _ in range(100):
		tmp.append(rand() )   #2018-4-29:随机初始化变为0.0初始化
	return tmp

def txt2vec(label,sentence_list): 
	#参数为：标签列表和 句子的词序列
	w2v=wload(vector_file)
	gvec=w2v.get_vector
	wordtable=w2v.vocab
	data_stream=[]
	print('2 \ read wordvec is over,start words->vector.')
	#word exchange to vector
	for sentence in sentence_list:
		tmp=[]
		count=0
		for words in sentence:
			if count<LENGTH:
				if words in wordtable:
					tmp.append( gvec(words) )
				else:
					tmp.append( rand_data() )
				count+=1
			else:
				break
		if count<LENGTH:
			for _ in range(LENGTH - count):
				tmp.append([0.0 for _ in range(100)])
		assert(len(tmp) == LENGTH )
		data_stream.append(tmp) 
	
	label_list=list( map(lambda x:map_num2class[x],label ) )   #need2change
	label_list=to_categorical(label_list,12)
	print(label_list[20:30])
	print('3 text changed to vector is over.')
	return np.asarray(label_list),np.asarray(data_stream)
	
def data_predeal(TRAIN_FILE):
	#读取文本，提取内容
	label=[]
	question=[]
	with open(TRAIN_FILE,encoding='utf-8') as f:
		train=f.readlines()
	for line in train:
		tmp=line.split(' ++$++ ')
		tmp1,tmp2=tmp[1:3]
		label.append(tmp1)
		question.append( list(cut(tmp2) ))
		#print(label,question);break;
	#统计类别数量
	for lbl in label:
		allclass.add(lbl)
	print('类别数量：',len(allclass),allclass)  #12
	
	mark=0
	for cla in allclass:
		map_num2class[cla]=mark
		mark+=1
	print('检验字典-数字映射：',len(map_num2class),map_num2class )
	#数值化
	label_num,matrix=txt2vec(label,question)
	
	#持久化
	with open(pickle_file,'ab') as data:
		dump(label_num,data)
		dump(matrix,data)
		print('dump 完成。')
	
#data_predeal(train_file);data_predeal(valid_file);data_predeal(test_file)




def build_model():
	#全连接神经网络
	with open(pickle_file,'rb') as data:
		label=load(data)
		matrix=load(data)
		v_out=load(data)
		v_in=load(data)
		test_out=load(data)
		test_in=load(data)
		
		print('数据长度：',len(label),'---',len(matrix) )
		print(label[100])
	act='relu'
	
	start=Input(shape=(40,100) )
	x=Dense(100,activation=act )(start)
	x=Dropout(0.2)(x)
	x=Dense(50,activation=act )(x)
	x=Dropout(0.4)(x)
	x=Dense(30,activation=act )(x)
	x=Flatten()(x)
	end=Dense(12,activation='softmax')(x)
	model_D=Model(inputs=start,output=end)
	model_D.summary()
	model_D.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy'])
	model_D.fit(matrix,label, epochs=10, batch_size=32,verbose=2,
				validation_data=(v_in,v_out)
				 )
	model_D.save('model.h5')
	

	yp = model_D.predict(test_in, batch_size=32, verbose=2)
	ypreds = np.argmax(yp, axis=1)
	ytrues=np.argmax(test_out,axis=1)

	targetnames = ['0medicare-insurance', '1health-insurance', '2other-insurance', '3disability-insurance', '4renters-insurance', '5retirement-plans', '6critical-illness-insurance', '7home-insurance', '8auto-insurance', '9annuities', '10life-insurance', '11long-term-care-insurance']
	print('多分类报告:')
	print(classification_report(ytrues, ypreds, target_names=targetnames,digits=5))
	print('混淆矩阵:')
	con_mat=confusion_matrix(ytrues, ypreds)   #混淆矩阵:行为真实类别,列为预测类别
	print(con_mat)

build_model()


'''
分类模型已经基本可用，下一步考录是否进一步分类。然后进行初步的分类器优化
统计一下训练语料中的每个类别的数量 。/返回回答：回答句子的生成
受答案的相似性的启发：选择相似的答案进行回答。
	无论是构建知识库，还是使用GAN都不是5天內可以完成的。
'''
ANSWER_FILE='answers.txt'
en_ans=[]
zh_ans=[]

def answer_deal():
	with open(ANSWER_FILE,encoding='utf-8') as f:
		answer=f.readlines()
	for line in answer:
		tmp=line.split(' ++$++ ')
		if len(tmp) <2: 
			continue
		tmp1,tmp2=tmp[1:]
		#print(tmp1)
		#print(tmp2)  #查看内容提取效果
		#break
		zh_ans.append(tmp1)
		#en_ans.append(tmp2)
label=[]
for i in range(12):
	label.append(set() )

def add_class_label():
	#添加类别标签，使用标签列表
	#还需 调整类别顺序
	nolabel=0  #统计无法识别的答案数量
	for iterm in zh_ans:
		if '汽车' in iterm:
			label[8].add(iterm)
		elif '人寿' in iterm:
			label[10].add(iterm)
		elif '健康' in iterm:
			label[1].add(iterm)
		elif '残疾' in iterm:
			label[3].add(iterm)
		elif '医疗' in iterm:
			label[0].add(iterm)
		elif '长期护理' in iterm:
			label[11].add(iterm)
		elif '年金' in iterm:
			label[9].add(iterm)
		elif '家庭' in iterm:
			label[7].add(iterm)
		elif '租' in iterm:
			label[4].add(iterm)
		elif '重大疾病' in iterm:
			label[6].add(iterm)
		elif '退休' in iterm:
			label[5].add(iterm)
		else:
			label[2].add(iterm)
			nolabel+=1
	print(len(label[5] ) )
	print('其他类别保险的数量：',nolabel)
	


'''
				QA应用系统
		使用问题模型识别 问题的类别标签。
		再从答案的候选中 选择一个。
	
'''
def predeal_one(quest):
	#字符串分词 并转化成词向量
	sentence=list(cut(quest ) )
	
	w2v=wload(vector_file)
	gvec=w2v.get_vector
	wordtable=w2v.vocab

	tmp=[]
	count=0
	for words in sentence:
		if count<LENGTH:
			if words in wordtable:
				tmp.append( gvec(words) )
			else:
				tmp.append( rand_data() )
			count+=1
		else:
			break
	if count<LENGTH:
		for _ in range(LENGTH - count):
			tmp.append([0.0 for _ in range(100)])
	assert(len(tmp) == LENGTH )
	return np.array( [tmp])
	
def question_type(quest):
	model_D=load_model('model.h5')
	return model_D.predict(quest,verbose=1)
	
import random
def main():
	answer_deal()
	add_class_label()
	#输入问题
	quest=input('输入保险类问题：')
	quest=predeal_one(quest)
	class_type=question_type(quest)  #找出类别标签
	result=list(label[np.argmax(class_type)])
	print(random.choice(result) )

main()


