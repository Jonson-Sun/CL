#！ -*- utf8 -*-
'''
	本文使用简单的保险问题问题预料
			构建一个简单的神经网络分类器
		目的：验证想法

'''
import warnings as wn
wn.simplefilter("ignore")

from pickle import load,dump
from keras.layers import Dense,Activation, Dropout,Flatten,Input
from sklearn.metrics import classification_report,confusion_matrix
from keras.initializers import zeros,ones,constant
from keras.initializers import RandomNormal,RandomUniform,orthogonal
from keras.initializers import he_normal
from keras.models import Model,load_model
import numpy as np
np.random.seed(1325)


pickle_file='pick_demo.bin'



def build_mod():
	#elu，relu,softplus,softsign,tanh,sigmoid,hard_sigmoid,linear
	#init：constant,RandomUniform，truncatedNormal，variancescaling
				# orthogonal[隨機正交矩陣]，identity，lecun__uniform,glorot_normal
				# he_normal,he_uniform
	act='relu'

	start=Input(shape=(40,100) )
	x=Dense(80,activation=act,kernel_initializer=he_normal() )(start)  #第一层很重要
	x=Dense(60,activation=act )(x)
	x=Dense(40,activation=act )(x)
	x=Dropout(0.2)(x)
	x=Dense(20,activation=act )(x)
	x=Flatten()(x)
	end=Dense(12,activation='softmax')(x)
	model_D=Model(inputs=start,outputs=end)
	return model_D


def build_model():
	with open(pickle_file,'rb') as data:
		label=load(data)
		matrix=load(data)
		v_out=load(data)
		v_in=load(data)
		test_out=load(data)
		test_in=load(data)

		print('数据长度：',len(label),'---',len(matrix) )
		print(label[100])

	model_D=build_mod()
	model_D.summary()
	#opt：sgd，rmsprop，adagrad,adadelta,adam,adamax,nadam,
	model_D.compile(loss='categorical_crossentropy',optimizer='nadam', metrics=['accuracy'])
	model_D.fit(matrix,label, epochs=200, batch_size=32,verbose=2,
				validation_data=(v_in,v_out)
				 )
	#model_D.save('model.h5')


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



print('主函数执行结束。')


