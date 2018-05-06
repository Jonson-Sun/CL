'''
	本文件实现卷积神经网络
		尝试一维滤波器 一维时域卷积。
'''
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from keras.models import Sequential,Model,load_model
from keras.layers import Dense,Activation
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import Input
from keras.layers.recurrent  import LSTM,GRU
from keras.layers import convolutional as conv
from keras.layers.pooling import GlobalAveragePooling2D,AveragePooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.merge import concatenate
from keras.callbacks import  EarlyStopping,ModelCheckpoint,TensorBoard,LearningRateScheduler
from keras.utils import plot_model

from data_predeal import data_ready,read_3d

import numpy as np
np.random.seed(134)   #相同的随机初始化,使结果可复现:

model_file='rtdata/model_CNNs.h5'

#----------------------------------------                  ----------------1、--------定义网络结构--------
def build2():
	#函数式模型
	inputshape= (40,100,1)
	start=Input(shape=inputshape )
	active='tanh'

	x1=conv.Conv2D(filters=4,kernel_size=(5,1),padding='same',activation=active)(start)
	#x1=conv.Conv2D(filters=4,kernel_size=(3,1),padding='same',activation=active)(x1)
	#x1=conv.Conv2D(filters=4,kernel_size=(2,1),padding='same',activation=active)(x1)
	#x1=BatchNormalization()(x1)
	#x1=GlobalAveragePooling2D()(x1)

	x2=conv.Conv2D(filters=4,kernel_size=(5,1),padding='same',activation=active)(start)
	#x2=AveragePooling2D((2,2) )(x2)
	x2=conv.Conv2D(filters=4,kernel_size=(3,1),padding='same',activation=active)(x2)
	#x2=conv.Conv2D(filters=4,kernel_size=(1,2),padding='same',activation=active)(x2)
	#x2=BatchNormalization()(x2)

	x3=conv.Conv2D(filters=4,kernel_size=(5,1),padding='same',activation=active)(start)
	#x3=AveragePooling2D((2,2) )(x3)
	x3=conv.Conv2D(filters=4,kernel_size=(3,1),padding='same',activation=active)(x3)
	x3=conv.Conv2D(filters=4,kernel_size=(2,1),padding='same',activation=active)(x3)
	#x3=BatchNormalization()(x3)

	x4=conv.Conv2D(filters=4,kernel_size=(5,5),padding='same',activation=active)(start)
	#x4=AveragePooling2D((2,2) )(x4)
	x4=conv.Conv2D(filters=4,kernel_size=(3,3),padding='same',activation=active)(x4)
	x4=conv.Conv2D(filters=4,kernel_size=(2,2),padding='same',activation=active)(x4)
	#x4=BatchNormalization()(x4)

	x5=concatenate([x1,x2,x3,x4] )
	x5=Flatten()(x1)
	end=Dense(4)(x5)
	model=Model(inputs=start,outputs=end)
	return model




def build1():
	#1维卷积
	inputshape= (40,100)
	active='elu'
	print('#添加层++++++++++++++++++++++++++++++++++++++++')
	model=Sequential()
	model.add(conv.Conv1D(filters=20,kernel_size=(10),input_shape=inputshape,activation=active))
	model.add(Dropout(0.2) )
	#model.add(conv.Conv1D(filters=20,kernel_size=(5),activation=active))
	#model.add(Dropout(0.2) )
	
	model.add(Flatten() )
	model.add(Dense(4) )
	model.add(Activation('softmax') )
	return model




def build():
	#2d卷积全连接模型
	inputshape= (40,100,1)
	active='relu'
	print('#添加层++++++++++++++++++++++++++++++++++++++++')
	model=Sequential()
	model.add(conv.Conv2D(filters=4,kernel_size=(6,6),input_shape=inputshape,activation=active))
	model.add(Dropout(0.3) )
	#model.add(conv.Conv2D(filters=1,kernel_size=(2,2),activation=active))  #,padding='same'
	#model.add(Dropout(0.3) )
	#model.add( AveragePooling2D(2,2)  )
	#model.add(BatchNormalization() )
	model.add(Flatten() )
	model.add(Dense(4) )
	model.add( Activation('softmax') )
	return model
	#82   81

#----------------------------------------                  ----------2、-------设置网络参数,和导入数据---------------
def schedule(epoch):
	#学习率规划器,返回学习率 keras没设置的化默认0.01
	#   ,LearningRateScheduler(schedule)
	rate=0.8/(epoch+1)

	return rate

def cnns_train():
	#input_train, output_train,input_dev,output_dev=data_ready() #first_time_run=True
	input_train, output_train,input_dev,output_dev=read_3d()
	print('#初始化模型++++++++++++++++++++++++++++++++++')
	model=build1()
	print('#编译模型++++++++++++++++++++++++++++++++++')
	model.compile(loss='categorical_crossentropy',optimizer='adam',
		metrics=['accuracy']) #'recall'
	model.summary()
	print('#训练模型++++++++++++++++++++++++++++++++++')
	#early_stop =EarlyStopping(monitor='loss', patience=2) 	#损失达到精度,patience轮后停止训练
	#checkpointer =ModelCheckpoint(filepath="cp_cnn_best.h5", verbose=2, save_best_only=True)
	hist=model.fit(input_train, output_train, epochs=300, batch_size=64
	   ,verbose=2,callbacks=[TensorBoard(log_dir='tmp1/')]
	   ,validation_data=(input_dev,output_dev) )

	model.save(model_file)   #将模型保存到指定文件
	
cnns_train()

#----------------------------------------                  --------3、------初步测试------------------

def parse_model():
	#用于训练完成后的后续操作
	model=load_model(model_file)
	model.summary()
	input_test,output_test=data_ready(test=True)
	#input_test,output_test=read_3d(test=True)
	print('#测试模型++++++++++++++++++++++++++++++++++++')
	score = model.evaluate(input_test, output_test, batch_size=32,verbose=2)
	print('损失loss：',score[0])
	print('准确率:accuracy:',score[1])
	#print('精确率pression：',score[2])
	print('召回率recall:',score[2])
	#F1=2*score[3]*score[2]/(score[3]+score[2])
	#print('F1_score:',F1)
	#对新的数据进行预测
	#classes = model.predict(x_test, batch_size=128)

	#print('#数据可视化:+++++++++++++++++++++++++++++++++++++')
	#plot_model(model,to_file='model.png')

#parse_model()
