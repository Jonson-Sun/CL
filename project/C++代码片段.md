# C++代码片段
## 位操作

```C
//==========================================
//				位(bit)操作
//功能:
//	可以用作信号表
//	安全性上讲vector<bool>更好,理由: 8个1的出错概率远小于一个1
//函数功能:
//		bit_value_get: 按位置取值
//		bits_show:整数的bit表示
//		bit_value_set: 按位置设值
//==========================================

//获取val 的第position位的值
template<typename T>
char bit_value_get(T val,int position) 
{
	int lens=sizeof(val)*8;
	assert(lens>=position);
	T label=1;
	label<<=(position-1);
	return (label&val ? '1' : '0'); //char
	//return (label&val ? 1 : 0); //int
	//return (label&val ? true : false); //bool
}

template<typename T>
void bits_show(T val) 
{
	int lens=sizeof(val)*8;
	//cout<<"bit长度"<<lens<<endl;
	
	T label=1;
	string result="";
	for(int i=0;i<lens;i++){
		result+=(label&val ? '1' : '0');
		label<<=1;  //移位检测
		//label*=2;
		//cout<<itos(label)<<endl;
	}
	reverse(result.begin(),result.end());
	cout<<result<<endl;
}

template<typename T>
bool bit_value_set(T& val,int position)  //将position的值 取反
{
	int lens=sizeof(val)*8;
	assert(lens>=position);
	
	T label=1;
	label<<=(position-1);
	
	return val^=label;
}


//bit操作的测试函数

bool bit_used()		
{
	short tmp=11;
	bits_show<short>(tmp);
	short i=1;
	while(i <= 16){
		bit_value_set<short>(tmp,i);
		bits_show<short>(tmp);
		i++;
	}
  return true;
	bits_show<long>(8848);
	bits_show<unsigned int>(8848);
	bits_show<int>(-8849); //负数->补码表示
	bits_show<short>(1);
	bits_show<int>(-1);
	bits_show<bool>(false);
	bits_show<bool>(true); //原来是8个1
	bits_show<char>('A');
	//string float double 不行,缺少<<= 和 float label=1 出错
	//string:可以使用stoi
	
	bits_show<int>(33);
	cout<<bit_value_get<int>(33,1)<<endl;
	cout<<bit_value_get<int>(33,9)<<endl;
  return true;
}
```

## C++11
```cpp
#include <iterator>
#include <algorithm>
#include<cassert>

//===========================================
//
//	C++11 学习整理
//
//
//===========================================
#include<array>
#include <unordered_map> //hash table实现
#include <unordered_set> //hash table实现

int used_auto(int a,int b)  //C++14开始 函数定义返回值也可为auto
{
	//int num_arr[]={1,2,3,4,5};
	array<int,9> num_arr={1,2,3,4,5};  //新数组
	for(auto num:num_arr)   //新形式的for循环
	{
		cout<<num<<" ";
	}
	cout<<endl;
	//lambda表达式
	auto twoplus=[](int a,int b){return a+b;};
	return twoplus(a,b);
}

#include<thread>
#include<chrono>
#include<atomic>  //无数据竞争
#include<future>
#include<vector>
//#include<unistd.h>
void called(){
	cout<<"函数开始"<<endl;
	this_thread::sleep_for(chrono::seconds(1));
	cout<<"函数结束"<<endl;
} 
bool multi_thread()  //多线程-static出现断错误
{
	thread myth {called};
	
	thread myth1{called};
	myth.join();
	myth1.join();
	
	//myth.detach();
	//myth1.detach();
	this_thread::sleep_for(chrono::seconds(5));
}
int canshu(vector<int>& vec,int x)
{
	auto asd=x;
	for(auto v:vec){
		asd+=v;
	}
	cout<<asd<<"是vecsum;"<<x<<"是长度,等待3s..."<<endl;
	this_thread::sleep_for(chrono::seconds(3));
	return asd;
}
bool test_cpp11()
{
	//cout<<"lambda's result:"<<used_auto(3,4)<<endl;
	//cout<<(NULL==0?"NULL是0":"不是0")<<endl;
	//nullptr : 空指针 类型
	//multi_thread();
	
	int aaa=23;
	vector<int> vec100={1,2,3,4,5,6,7,8};
	//auto result_future=async(canshu,ref(aaa));  //传递引用
	auto result_future=async(canshu,ref(vec100),vec100.size());
	cout<<result_future.get()<<"是返回的结果"<<endl;
	return true;
}
//============================================

```



---

##结束
