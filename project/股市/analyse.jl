# 本文件为Julia程序设计语言源文件 

#=====================================
金融数据处理: 
	1,下载大盘数据:download_data.py 
		关键:url="http://hq.sinajs.cn/list=sh601006"  
		美股的股票代码为字母:有待进一步分析 
		    
	2,分析股市数据
		只处理上证和深证,由于存在时间差,暂不分析港股;
		统计量使用均值和标准差;(加权的话可能有偏见)
		给股票加权就是偏见:国企权重高,股市必然稳定,反之亦然
		
	3,本部分只计算  均值和标准差  原因
		本文抽取市场最重要的信息,就是当前股票价格;
		计算当前股票价格的均值可以看出市场的整体走势;
		计算当前股价的标准差可以看出市场的稳定情况;
		(由于本身包含了相关的指数(上证指数)信息,不再有加权的意义)
		
	4,使用PyPlot画图展示结果	
		加载太慢!
		
	5,标准差std计算公式 :sqrt(sum((v.-mean(v)).^2)/(length(v)-1))==std(v)
		标准库文档中的公式是错的:sqrt(sum((v - mean(v)).^2) /(length(v) - 1))
	
	6,常用计算方法:
		采样,加权,程序计算
		
	7,自注释编码???
	
	8,这种简单粗暴的统计方式:
		因为不同部分获得的比例过大,会影响统计结果,例如成交额
		沪市的债券,指数所占的比例过大
		
==================================#
import Statistics.std  
import Statistics.mean  #均值
import Statistics.median #中位数
import Serialization.serialize
import Serialization.deserialize
import Dates.now 

#=================================
	画图:
		展示的图像仍需手动关闭
		因此只在结尾调用一次
	加载PyPlot大约需要21s
==============================#

import PyPlot.plot  #pyplot严重拖慢启动时间
import PyPlot.xlabel
import PyPlot.ylabel
import PyPlot.title

function 展示结果()
	list_sh=deserialize("tmp_sh")
	list_sz=deserialize("tmp_sz")
	sh_m=[arr[1] for arr in list_sh]
	sh_s=[arr[2] for arr in list_sh]
	sz_m=[arr[1] for arr in list_sz]
	sz_s=[arr[2] for arr in list_sz]
	
	plot(sh_m,"bo--")  #上证均值
	show()
	plot(sh_s,"ko--")	#上证
	show()
	plot(sz_m,"bo--")	#深证均值
	show()
	plot(sz_s,"ko--")	#深证
	show()
	
	@info "均值	  最小值	 最大值	 中值	终值   初值"
	str=""
	for arr in [sh_m,sh_s,sz_m,sz_s]
		tmp=round(mean(arr),digits=4),minimum(arr),maximum(arr),
		median(arr),arr[length(arr)],arr[1]
		@info tmp
		str=str*repr(tmp)*"\n"
	end
	open("log.txt","a") do io
		str=str*repr(now())*"\n\n"
		write(io,str)
	end
end
function 展示结果(list_sh,list_sz)
	plot([arr[1] for arr in list_sh])  #上证均值
	show()
	plot([arr[2] for arr in list_sh])	#上证标准差
	show()
	plot([arr[1] for arr in list_sz])	#深证均值
	show()
	plot([arr[2] for arr in list_sz])	#深证标准差
	show()
end

#===========================
	功能:
		"1024" -> 1024
		"1.6189" -> 1.6189
=========================#
function 符数转换(数字串:: SubString{String})
	#@info typeof(数字串)
	number::Float64=0.0
	小数=false
	指数=1
	进制=10
	table=Dict('0'=>0,'1'=>1,'2'=>2,'3'=>3,'4'=>4,'5'=>5,
	        '6'=>6,'7'=>7,'8'=>8,'9'=>9)   
	for item in 数字串
		if item == '.'   小数=true;指数=0;进制=1;number/=10;continue; end
		if 小数 == true 指数-=1 end
	    number=number*进制 + table[item]*(10.0^指数)
	end
	return round(number,digits=4)
end

#===========================
	抽取下载的股票信息
	进行统计计算
=========================#

function 分析股市1(文件名,类型::Int=4)
	#类型为2:3是昨天收盘价与今天收盘价的变化
	function 获取数据(列::Int)
		# 2:昨日收盘价格;
		# 4:当前价格;
		# 3:今日收盘价格
		数据列=[]
		for 行 in eachline(文件名)
		  try
			单数据=split(行,",")
			tmp= 符数转换(单数据[列])
			#if tmp<0.01 continue end #去掉不变项(变化过小的项)
			push!(数据列,tmp)
		  catch e 
	  		@info "出现异常:$(e)"
	  		continue
	  	  end
		end
		return 数据列
	end
		
	当前价格向量=获取数据(类型)
	
	当前均值=mean(当前价格向量)
	#当前标准差=std(当前价格向量)# 意义不大
	#几何均值=sqrt(sum([x^2 for x in 当前价格向量]))
	#股市的平均变化率=mean(当前价格向量./获取数据(2))
	 	#当前价格/昨日收盘价格(也可以是今日开盘价)  维度不匹配???
	变化率=sum(当前价格向量)/sum(获取数据(2))
	
		
	return round(当前均值,digits=4),round(变化率,digits=4)
end
#==============================================

	按照给定的 运行时间 运行分析程序
		分析股市函数的包装

==========================================#
function 实时分析(运行时间::Float64=60.0)
	上证="shdata.txt"
	深证="szdata.txt"
	list_sh,list_sz=[],[]	
	
	#for i=1:80  #10次一分钟 ?如何精确控制时间?
	t1=time()
	时长=0.1
	while 时长 < 运行时间  #时间单位为分钟
		run(`rm -f shdata.txt`)
		run(`rm -f szdata.txt`)
		try
			run(`./download_data.py`)
		catch e
			@error "下载出错,忽略:$e"
			continue
		end
		
		num1=分析股市1(上证)
		push!(list_sh,num1)
		num2=分析股市1(深证)
		push!(list_sz,num2)
		
		sleep(30)
		
		t2=time()
		时长=round((t2-t1)/60)
		@info "运行$(时长)分钟;结果:$(num1),$(num2)"
		
		#展示结果(list_sh,list_sz) 
		#去掉上一行的注释"#:  即可展示实时的股市态势
		
	end
	#序列化与反序列化
	serialize("tmp_sh",list_sh)
	serialize("tmp_sz",list_sz)
	#list_sh=deserialize("tmp_sh")
	#list_sz=deserialize("tmp_sz")
end






实时分析(121.0)

展示结果()














#===============================================
	第二部分:进一步分析
	
		1.计算两天(昨日,当日)的收盘价情况
		2.华尔街见闻上有完整的时图,日图,月图(统计方法可能有差异)
			重复计算意义不大
	下一步:
		3.可以在收盘后 统计 最高价-最低价 来计算波动幅度
			mean(获取数据(5)./获取数据(6))
			
		4.可以计算{成交的股票数(9),成交金额(10)}
			来统计市场的活跃程度:
			平均每股成交价=mean(获取数据(10)./获取数据(9))
			
		5.可以计算{买一->买五,卖一->卖五}
			来查看人们的购买意愿和卖出意愿
			
		6.时间戳信息可以在归档中使用(暂时没用)
		
	然后?
=============================================#
function 获取数据(文件名,列::Int)
	# 2:昨日收盘价格;
	# 3:今日收盘价格
	数据列=[]
	for 行 in eachline(文件名)
	  try
		单数据=split(行,",")
		tmp= 符数转换(单数据[列])
		if tmp<0.01 continue end #去掉不变项(变化过小的项)
		push!(数据列,tmp)
	  catch e 
  		@info "出现异常:$(e)"
  		continue
  	  end
	end
	return 数据列
end

function 统计两种价格(文件名,col1=3,col2=4)  #实现功能1
	价格向量1=获取数据(文件名,col1)
	均值1=mean(价格向量1)
	标准差1=std(价格向量1)
	
	价格向量2=获取数据(文件名,col2) 
	均值2=mean(价格向量2)
	标准差2=std(价格向量2)

	@info "统计中包含指数变化"
	#@show 价格向量1[rand(1:100)]
	@show length(价格向量1)
	@show length(价格向量2)
		
	@show round(均值1,digits=4)
	@show round(均值2,digits=4)
	@show round(标准差1,digits=4)
	@show round(标准差2,digits=4)

end
import Dates.hour
import Dates.minute
import Dates.now
function test()
	while true
		if hour(now())==9 && minute(now())==27 run(`julia analyse.jl`);break; end
		if hour(now())==1 && minute(now())==0  run(`julia analyse.jl`);break; end
	end
  return
	上证="szdata.txt"
	tmp=分析股市1(上证)
	@info "(均值,变化率):$tmp"

  return 
  
	文件名="szdata.txt"
	tmp_arr=获取数据(文件名,5)./获取数据(文件名,6)
	
	plot(tmp_arr,"bo");xlabel("sample");ylabel("x/y");title("market value");show();
	plot(sort!(tmp_arr));show();
	
	tmp=round(mean(tmp_arr)*100-100.0,digits=4)
	@info "平均价格变化率(百分比):$(tmp) %"
	
	tmp=获取数据(文件名,10)./获取数据(文件名,9)
	平均每股成交价=round(mean(tmp),digits=4)
	@show 平均每股成交价
	
	plot(tmp,"bo-");show();
	plot(sort!(tmp),"bo-");show();
	
	tmp=获取数据(文件名,10)
	@info "总成交额:$(round(sum(tmp)/10000_0000,digits=4) )亿" #/10000
	plot(tmp,"bo-");show();
	plot(sort!(tmp),"bo-");show();
	
	tmp=获取数据(文件名,9)
	@info "总成交数:$(round(sum(tmp)/100_0000,digits=4) )万手" #/100 为手数
	plot(tmp,"bo-");show();
	plot(sort!(tmp),"bo-");show();
	
	
  return 
	
	@info "测试函数开始执行"
	上证="sh_finace.txt"
	深证="sz_finace.txt"
	
	统计两种价格(上证,4,5)  #????
	统计两种价格(深证,3,5)  #????
	
	@info "函数执行结束"
end
#test()


#=============================

error:
  1.Remote end closed connection without"
	http.client.RemoteDisconnected: 
		Remote end closed connection without response
  解决方法 : 减少采样次数:30s一次:2h->240个采样点

  2.raise RemoteDisconnected:
  	解决方法: 通过trycatch 忽略异常情况
		sina有反拉取机制???
==========================#