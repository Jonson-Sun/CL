'''
	全连接神经网络
		device_count, 告诉tf Session使用CPU数量上限
		
'''
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
'''
#为了更加充分的利用cpu进行的优化设置:没用
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
KTF.set_session(tf.Session(config=tf.ConfigProto(device_count={'cpu':1},
	inter_op_parallelism_threads=1,
	intra_op_parallelism_threads=1 ) ) )
'''


from keras.models import Sequential,load_model
from keras.layers import Dense,Activation, Dropout,Flatten
from keras.utils import to_categorical
from keras.callbacks import  TensorBoard
from pickle import load
import numpy as np
np.random.seed(1432)

pickle_file1='rtdata/train_dev_test40.bin'
model_file='rtdata/dense_model.h5'
#--------------------------------+++++++++++++++++++++++++----------------------------

def read_data(train=True):
	LENGTH=40
	#从文件中顺序获得对象
	with open(pickle_file1,'rb') as data:
		input_train=load(data)
		output_train=load(data)
		input_dev=load(data)
		output_dev=load(data)
		input_test=load(data)
		output_test=load(data)
	#对象进行规格化处理
	size=len(input_train)
	input_train=input_train.reshape(size,LENGTH,100)
	size0=len(input_dev)
	input_dev=input_dev.reshape(size0,LENGTH,100)
	size1=len(input_test)
	input_test=input_test.reshape(size1,LENGTH,100)
	
	print('三个集合的大小:',size,size0,size1)
	#根据用途选择返回值
	if train is True:
		return input_train,output_train,input_dev,output_dev
	else:
		return input_test,output_test
		
		
#---------------------------+++++++++++++++++++++++++++------------------------------

def all_connect_net_train():
	''' 尝试用dence 进行分类
			本函数只负责训练模型：改一下层数看看效果
	'''
	input_train,output_train,input_dev,output_dev=read_data()
	act='relu'
	bias=False
	
	model=Sequential()
	model.add(Dense(100,input_shape= (40,100), activation=act,use_bias=bias ))
	model.add(Dropout(0.4))
	model.add(Dense(100,activation=act ))
	model.add(Dropout(0.4))
	model.add(Dense(100,activation=act ))
	model.add(Dropout(0.4))
	model.add(Flatten() )
	model.add(Dense(4) )
	model.add( Activation('softmax') )
	
	model.compile(loss='categorical_crossentropy',optimizer='adam', metrics=['categorical_accuracy','recall'])
	#轮数应该增加试试
	model.fit(input_train, output_train, epochs=500, batch_size=64,verbose=2,
				validation_data=(input_dev,output_dev),
				callbacks=[TensorBoard(log_dir='/home/asen/tmp') ]
				 )
	#打印模型概况
	model.summary()
	#保存权重参数:
	model.save(model_file)

#--------------------------------+++++++++++++++++++++++++----------------------------

def net_test():
	#从文件载入参数
	print('测试从文件中载入模型参数')
	input_test,output_test=read_data(False)
	model=load_model(model_file)
	score = model.evaluate(input_test, output_test, batch_size=32,verbose=2)
	print('dev损失：',score[0])
	print('dev准确率：',score[1])
	print('dev召回率:',score[2])
	
	F=2*score[1]*score[2]/(score[1]+score[2])
	print("F-score:",F)
#--------------------------------+++++++++++++++++++++++++----------------------------
all_connect_net_train()
net_test()


'''
	axis:辨析
		mean(axis=1),我们将得到按行计算的均值
		drop((name, axis=1),我们实际上删掉了一列
	recall_1:
	"`Tensor` objects are not iterable when eager execution is not "
			TypeError: `Tensor` objects are not iterable when eager execution is not enabled.
 			To iterate over this tensor use `tf.map_fn`
 	recall_2:
 	TypeError: object of type 'Tensor' has no len()
'''

