def build_model():
	#两层宽的网络也可以达到87.3%
	act='relu'
	start=Input(shape=(30,100) )
	x=Dense(300,activation=act,return_sequences=True )(start)
	x1=Dropout(0.2)(x)  #88.9=20  89.46=30
	
	x=Dense(200,activation=act,return_sequences=True )(x1)
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
