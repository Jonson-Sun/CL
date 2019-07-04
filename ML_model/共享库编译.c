

#include"stdio.h"

int add(int a ,int b)
{
	return ( a+b);
}

void cprint(char*  asd,int n)
{
	int cunt=0;
	while(cunt++ <n ){
		printf("%s",asd);
		asd+=4;  //python里面每个字符占四个字节
	}
	printf("\n");
}


//int main(){ cout<<"文件开始执行"<<endl;return 0;}
//gcc -shared -fpic obj.c -o obj.so
//c++编译后的文件会把函数名改名（为了实现重载功能)  undefined symbol