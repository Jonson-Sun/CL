#！ -*- utf8 -*-
'''
	本文档格式为 python3 脚本文档
		2018-4-3: 23:08
'''
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense,Activation
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers.recurrent  import LSTM
from keras.layers.recurrent  import GRU
from keras.layers.recurrent  import SimpleRNN
from keras.callbacks import  EarlyStopping
from keras.callbacks import ModelCheckpoint

from data_predeal import PICKLE_FILE,LENGTH,read_3d
import numpy as np
np.random.seed(1432)


#model_file='rtdata/GRU_model.h5'
#model_file='rtdata/simple_RNN_model.h5'
model_file='lstm_best.h5'


#--------------------------------+++++++++++++++++++++++++-------------1、---------------
def simple_rnn(model):
	print('the simple RNN struct :')
	
	model.add(SimpleRNN(60,input_shape=(LENGTH,100),return_sequences=True,activation='relu')  )
	model.add(Dropout(0.3) )
	model.add(SimpleRNN(50,return_sequences=True,activation='relu')  )
	model.add(Dropout(0.3) )
	model.add(SimpleRNN(40,return_sequences=True,activation='relu')  )
	model.add(Dropout(0.3) )
	model.add(SimpleRNN(30,return_sequences=True,activation='relu')  )
	model.add(Dropout(0.3) )
	model.add(SimpleRNN(20,return_sequences=True,activation='relu')  )
	model.add(Dropout(0.3) )
	model.add(SimpleRNN(10,return_sequences=True,activation='relu')  )
	#87
	return model

def lstm_used(model):
	print('pure LSTM struct :')
	act='elu'
	rate=0.4
	model.add(LSTM(20,input_shape=(LENGTH,100),return_sequences=True,activation=act  ) )
	model.add(Dropout(rate) )
	model.add(LSTM(32,return_sequences=True,activation=act  ) )
	model.add(Dropout(rate) )
	model.add(LSTM(16,return_sequences=True,activation=act  ) )
	model.add(Dropout(rate) )
	model.add(LSTM(8,return_sequences=True,activation=act  ) )
	model.add(Dropout(rate) )
	model.add(LSTM(4,return_sequences=True,activation=act  ) )
	model.add(Dropout(rate) )
	return model

def gru_used(model):
	#91
	print('pure GRU struct :')
	
	model.add(GRU(20,input_shape=(LENGTH,100),return_sequences=True,activation='relu')  )
	model.add(Dropout(0.3)  )
	model.add(GRU(15,return_sequences=True,activation='relu')  )
	model.add(Dropout(0.3)  )
	model.add(GRU(10,return_sequences=True,activation='relu')  )
	model.add(Dropout(0.3)  )
	'''
	model.add(GRU(8,return_sequences=True,activation='relu')  )
	model.add(Dropout(0.2)  )
	model.add(GRU(6,return_sequences=True,activation='relu')  )
	model.add(Dropout(0.2)  )
	model.add(GRU(4,return_sequences=True,activation='relu')  )
	'''
	return model

#--------------------------------+++++++++++++++++++++++++---------------2、-------------

def rnn_train():
	#循环神经网络 使用
	input_train,output_train,input_dev,output_dev=read_3d(test=False)
	model=Sequential()

	model=lstm_used(model)
	#model=gru_used(model)
	#model=simple_rnn(model)
	
	model.add(Flatten() )
	model.add(Dense(4))
	model.add(Activation("softmax") )
	
	model.compile(loss='categorical_crossentropy',optimizer='adam', metrics=['categorical_accuracy','recall'])
	model.summary()
	early_stop =EarlyStopping(monitor='loss', patience=2)
	checkpointer =ModelCheckpoint(filepath=model_file, verbose=0, save_best_only=True)
	model.fit(input_train, output_train, epochs=150, batch_size=64,verbose=2
			,validation_data=(input_dev,output_dev),callbacks=[])

	model.save(model_file)

#--------------------------------+++++++++++++++++++++++++------------3、----------------

def rnn_dev():
	#测试集验证模型
	input_test,output_test=read_3d(test=True)
	model = load_model(model_file)
	model.summary()
	score = model.evaluate(input_test, output_test, batch_size=128,verbose=2)
	print('测试损失：',score[0])
	print('测试准确率：',score[1])
	#print('evaluate RESULT:',score)
	print('召回率:',score[2])
	F=2*score[1]*score[2]/(score[1]+score[2])
	print("F-score:",F)

#--------------------------------+++++++++++++++++++++++++----------------------------
rnn_train()
rnn_dev()


