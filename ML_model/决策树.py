#author: xiaolinhan_daisy
#date: 2017/12/25
#site: YueJiaZhuang
from numpy import *

def createDataSet():
	# datalist ???
    dataSet = [[1, 1,'one'],
               [1, 1,'two'],
               [1, 0,'one'],
               [0, 1,'one'],
               [1, 0,'two']]
               
    labels = ['round','red']
    return dataSet, labels

#计算数据集的entropy
def calcEntropy(dataSet):
    totalNum = len(dataSet)
    labelNum = {}
    entropy = 0
    for data in dataSet:
        label = data[-1]  #获得分类结果
        if label in labelNum:
            labelNum[label] += 1  #统计频次
        else:
            labelNum[label] = 1

    for key in labelNum:
        p = labelNum[key] / totalNum  #计算概率
        entropy -= p * log2(p)  #带入公式计算熵
    return entropy

def calcEntropyForFeature(featureList):
    totalNum = len(featureList)
    dataNum = {}
    entropy = 0
    for data in featureList:
        if data in dataNum:
            dataNum[data] += 1
        else:
            dataNum[data] = 1

    for key in dataNum:
        p = dataNum[key] / totalNum
        entropy -= p * log2(p)
    return entropy  #特征自身的离散度




def splitDataSetByFeature(i, dataSet):
    subSet = {}  
    feature = [data[i] for data in dataSet]
    for j in range(len(feature)):    # 此处直接for循环feature 更好
        if feature[j] not in subSet:
            subSet[feature[j]] = []  #特征第一次出现

        splittedDataSet = dataSet[j][:i]
        splittedDataSet.extend(dataSet[j][i + 1:])
        subSet[feature[j]].append(splittedDataSet)  #加入的是去掉特征j后的子集
    return subSet   #特征的 多个list 集合
#  两种特征选择方法
#选择最优划分属性ID3
def chooseBestFeatureID3(dataSet, labels):  #1
    bestFeature = 0
    initialEntropy = calcEntropy(dataSet)  #集合的总的熵值
    biggestEntropyG = 0
    
    for i in range(len(labels)):
        currentEntropy = 0
        feature = [data[i] for data in dataSet] #第i列
        subSet = splitDataSetByFeature(i, dataSet)
        totalN = len(feature)
        for key in subSet:
            prob = len(subSet[key]) / totalN  #特征相同的元素数/样本总数
            currentEntropy += prob * calcEntropy(subSet[key])
        #数据集的离散度-本列以外的离散度  特征的离散度也要由周围环境来刻画?   
        entropyGain = initialEntropy - currentEntropy  
        if(biggestEntropyG < entropyGain):
            biggestEntropyG = entropyGain
            bestFeature = i
    return bestFeature

#选择最优划分属性C4.5
def chooseBestFeatureC45(dataSet, labels):
    bestFeature = 0
    initialEntropy = calcEntropy(dataSet)
    biggestEntropyGR = 0
    
    for i in range(len(labels)):
        currentEntropy = 0
        feature = [data[i] for data in dataSet]
        entropyFeature = calcEntropyForFeature(feature)
        subSet = splitDataSetByFeature(i, dataSet)
        totalN = len(feature)
        for key in subSet:
            prob = len(subSet[key]) / totalN
            currentEntropy += prob * calcEntropy(subSet[key])
            
        entropyGain = initialEntropy - currentEntropy
        entropyGainRatio = entropyGain / entropyFeature  #比ID3复杂:计算的是 周围离散度/自身离散度

        if(biggestEntropyGR < entropyGainRatio):
            biggestEntropyGR = entropyGainRatio
            bestFeature = i
    return bestFeature







def checkIsOneCateg(newDataSet):  #2
    flag = False
    categoryList = [data[-1] for data in newDataSet] #类别列表
    category = set(categoryList)
    if(len(category) == 1):
        flag = True  #同属一个集合了
    return flag

def majorityCateg(newDataSet):
    categCount = {}
    categList = [data[-1] for data in newDataSet]
    for c in categList:
        if c not in categCount:
            categCount[c] = 1
        else:
            categCount[c] += 1
    sortedCateg = sorted(categCount.items(), key = lambda x:x[1], reverse = True)

    return sortedCateg[0][0]  #概率最大的类
#创建ID3树
def createDecisionTreeID3(decisionTree, dataSet, labels):
    bestFeature = chooseBestFeatureID3(dataSet, labels)
    decisionTree[labels[bestFeature]] = {}
    currentLabel = labels[bestFeature]
    
    subSet = splitDataSetByFeature(bestFeature, dataSet)
    del(labels[bestFeature])
    newLabels = labels[:]
    for key in subSet:
        newDataSet = subSet[key]
        flag = checkIsOneCateg(newDataSet) #2
        if(flag == True):
            decisionTree[currentLabel][key] = newDataSet[0][-1]  #标记分类结果
        else:
            if (len(newDataSet[0]) == 1): #无特征值可划分
                decisionTree[currentLabel][key] = majorityCateg(newDataSet)
            else:
                decisionTree[currentLabel][key] = {}
                createDecisionTreeID3(decisionTree[currentLabel][key], newDataSet, newLabels)

# 创建C4.5树
def createDecisionTreeC45(decisionTree, dataSet, labels):
    bestFeature = chooseBestFeatureC45(dataSet, labels)
    decisionTree[labels[bestFeature]] = {}
    currentLabel = labels[bestFeature]
    subSet = splitDataSetByFeature(bestFeature, dataSet)
    del (labels[bestFeature])
    newLabels = labels[:]
    for key in subSet:
        newDataSet = subSet[key]
        flag = checkIsOneCateg(newDataSet)
        if (flag == True):
            decisionTree[currentLabel][key] = newDataSet[0][-1]
        else:
            if (len(newDataSet[0]) == 1):  # 无特征值可划分
                decisionTree[currentLabel][key] = majorityCateg(newDataSet)
            else:
                decisionTree[currentLabel][key] = {}
                createDecisionTreeC45(decisionTree[currentLabel][key], newDataSet, newLabels)





#测试数据分类
def classifyTestData(decisionTree, testData):
    result1 = decisionTree['round'][testData[0]]
    if(type(result1) == str): category = result1
    else:
        category = decisionTree['round'][testData[0]]['red'][testData[1]]
    return category
	#由于该函数编写的简单所以不要改训练数据
	#只通过"red"就可以分类的函数一开始就错了 KeyError:'round'
	#此外: 构建完成决策树后应该返回每一级的标签

if __name__ == '__main__':
    dataSetID3, labelsID3 = createDataSet()
    testData1 = [0, 1]
    testData2 = [1, 0]
    
    
  #创建ID3决策树
    bestFeatureID3 = chooseBestFeatureID3(dataSetID3, labelsID3)
    print("main bestfeature:",bestFeatureID3)
    decisionTreeID3 = {}
    createDecisionTreeID3(decisionTreeID3, dataSetID3, labelsID3)
    print("ID3 decision tree: ", decisionTreeID3)
  #测试决策树效果 
    category1ID3 = classifyTestData(decisionTreeID3, testData1)
    print(testData1 , ", classified as by ID3: " , category1ID3)
    category2ID3 = classifyTestData(decisionTreeID3, testData2)
    print(testData2 , ", classified as by ID3: " , category2ID3)
    
    
  #创建C4.5决策树
    dataSetC45, labelsC45 = createDataSet()
    bestFeatureC45 = chooseBestFeatureC45(dataSetC45, labelsC45)
    decisionTreeC45 = {}
    createDecisionTreeC45(decisionTreeC45, dataSetC45, labelsC45)
    print("C4.5 decision tree: ", decisionTreeC45)
  #测试决策树效果 
    category1C45 = classifyTestData(decisionTreeC45, testData1)
    print(testData1 , ", classified as by C4.5: " , category1C45)
    category2C45 = classifyTestData(decisionTreeC45, testData2)
    print(testData2 , ", classified as by C4.5: " , category2C45)
    
    
#  
#
#	优点:命名规范,不拖沓
#	不足:仅用于演示,不通用.
#
#
#		2019-3-30
#   