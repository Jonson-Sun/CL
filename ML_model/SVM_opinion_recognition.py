'''
			使用支持向量机进行意见分类
				对比神经网络的效果。
'''

from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from pickle import load
import numpy as np
np.random.seed(1432)


pickle_file1='rtdata/train_dev_test40.bin'

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
	#输入数据进行规格化处理
	size=len(input_train)
	input_train=input_train.reshape(size,LENGTH*100)
	size0=len(input_dev)
	input_dev=input_dev.reshape(size0,LENGTH*100)
	size1=len(input_test)
	input_test=input_test.reshape(size1,LENGTH*100)
	#输出标签格式化
	output_train=np.argmax(output_train,axis=-1)
	output_dev=np.argmax(output_dev,axis=-1)
	output_test=np.argmax(output_test,axis=-1)
	print('三个集合的大小:',size,size0,size1)
	#根据用途选择返回值
	if train is True:
		return input_train,output_train,input_dev,output_dev
	else:
		return input_test,output_test
		
		
def svm_used():
	'''
		1、将数据导入支持向量机
		2、ValueError: Found array with dim 3. Estimator expected <= 2.  : 输入的是向量
		3、参数介绍：
		SVC(C=1.0, kernel=’rbf’, degree=3, gamma=’auto’, coef0=0.0, shrinking=True,
				 probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, 
				 max_iter=-1, decision_function_shape=’ovr’, random_state=None）
			C\误差项的惩罚参数，一般取值为10的n次幂，如10的-5次幂
			kernel：linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’
			degree ：poly核，多项式的最高次数，默认为三次多项式
			tol：误差项达到指定值时则停止训练，默认为1e-3，即0.001。
			probability：是否采用概率估计。必须在fit（）方法前使用
			verbose：是否启用详细输出。
			max_iter:强制设置最大迭代次数。默认设置为-1，表示无穷大迭代次数
			
	'''
	input_train,output_train,input_dev,output_dev=read_data()
	model = OneVsRestClassifier( SVC(kernel='linear',verbose=True,probability=False)  )
	classifier=model.fit(input_train,output_train)
	
	rate=classifier.score(input_dev,output_dev)
	print('模型的平均争取率：',rate*100)
	'''
	二分类结果：0.39903846153846156
	多分类结果：0.7115384615384616  ：kernel='rbf'
							
	'''
	input_test,output_test=read_data(train=False)
	pred=classifier.predict(input_test)
	print(type(pred))
	targetnames = ['原因', '细节', '建议','条件']
	print('多分类报告:')
	print(classification_report(output_test, pred, target_names=targetnames))
	print('混淆矩阵:')
	con_mat=confusion_matrix(output_test, pred)   #混淆矩阵:行为真实类别,列为预测类别
	print(con_mat)
	
svm_used()
