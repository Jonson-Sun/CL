
#     			滚动新闻整理

#	对网络信息进行 自动 抓取,处理,分析,并生成报告


# 1. 下载,提取,归档
# 2. 分析想法:
#		1.按照标签 做 深度学习分类器
#		2.下载链接 内容到本地,处理html,做 内容摘要
#		3.
# 3. 可视化展示




#
#
#
#	本文件为 对 功能1 的代码实现
#
#
#
function 空文件检测(文件名)
	if filesize(文件名)<10
		return true
	else
		return false
	end
end
function 下载信息(INFO_URL,文件名)
	出错次数=0
	try
		download(INFO_URL,文件名)
		if 空文件检测(文件名)
			throw("所下载文件为空!!!")
		end
	catch e
			@error "下载出错: $e"
	end
end


function 提取时间(item)
	pattern=r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}"
	m=match(pattern,item)
	result=m.match
	#@info result
	return result
end
function 提取link(item)
	pattern=r"http:.+?html"
	m=match(pattern,item)
	result=m.match
	#@info result
	return result
end
function 提取类型标签(item)
	pattern=r">\w{2}</a>\]"
	m=match(pattern,item)
	result=m.match
	#@info result[2:5]
	return result[2:5]
end
function 提取title(item)
	pattern=r"title=\".+?\""
	m=match(pattern,item)
	result=m.match
	result=result[7:end]
	if (',' in result)
		tmp=""
		for iter in result
			if iter ==','
				tmp=tmp*' '
			else
				tmp=tmp*iter
			end
		end
		result=tmp
	end
	#@info result[8:end-3]
	return result
end
function 内容提取(文件名)
	#正则表达式提取 "时间,标签,title"
	str_tmp=""
	str_vec=String[]
	[str_tmp=str_tmp*line for line in readlines(文件名)]
	@info "文本文件长度: $(length(str_tmp))"
	
	regex=r"<li>\s*?<span>.+?</li>?"
	context=[m.match for m=eachmatch(regex,str_tmp)]
	#@info  context[1],context[3] #?
	for item in context
		#@info "子项$(length(item))"
		time=提取时间(item)
		type_finace=提取类型标签(item)
		title=提取title(item)
		link=提取link(item)
		
		push!(str_vec,time*','*type_finace*','*title*','*link)
		#break
		#注意:应在保存前,检查 内部逗号 的存在
		@assert !(',' in time) "提取的 时间序列 中包含逗号"
		@assert !(',' in type_finace) "提取的 类型标签 中包含逗号!"
		@assert !(',' in title) "提取的 标题 中包含逗号!"   #这种情况还真出现了
		@assert !(',' in link) "提取的 链接 中包含逗号!"
	end
	return str_vec
end


function 数据归档(str_vec,文件名="经济新闻.txt")
	归档内容="###归档分割标记==============\n"
	for term in str_vec
		归档内容=归档内容*term*"\n"
	end
	open(文件名,"a") do io
		write(io,归档内容)
	end
end


function test_1()
	下载地址="http://roll.eastmoney.com/"
	文件名="info_get_tmp.html"
	内容向量=String[]
	
	# 可以设置为半个小时执行一次
	# 如果长期运行出错:
	#	将下面的代码块 添加try..for.end  catch finally 每日归档
	
	for i=1:(30*6)  #采样次数
		下载信息(下载地址,文件名)
		str_vec=内容提取(文件名)
		#去除重复项
		#reverse和pushfirst 目的是保持内容的时间顺序
		for item in reverse(str_vec)
			if item in 内容向量 continue end
			pushfirst!(内容向量,item)
		end
		rm("文件名",force=true)
		@info "当前内容条数为 $(length(内容向量)),第$(i)次执行等待中 ..."
		sleep(115)  #采样间隔
		if i%120==0
			数据归档(内容向量)
			内容向量=String[]
		end
	end
	数据归档(内容向量)
	#三小时,180次采样无差错
	@info "测试函数运行完成"
end
test_1()


#
#
#	本部分功能的相关优化:
#		1.html格式转换为txt文档格式:
#			1.去掉所有的<.*>
#			2.去掉<style>.*</style>
#			3.去掉<script>.*<.script>
#
#		2.提取标签内容的通用函数:
#			1.get_label_context()
#			总结:正则表达式的应用场景:格式化的规范文本
#

function html2txt(文件名)
	str_tmp=open(f->read(f, String), 文件名)
	@info "文件字符串的长度为:$(length(str_tmp))"
	# 去掉所有的css和脚本
	pattern1=r"<style.+</style>|<script.+</script>"s  #s后缀:.匹配任意字符,包括换行
	pattern2=r"<.+?>|</.+?>"s
	tmp=replace(replace(str_tmp,pattern1=>s""),pattern2=>s"")
	tmp=split(tmp,"\n")
	
	str_tmp=""
	for line in tmp
		line=lstrip(line)
		if length(line) ==0 
			continue
		else
			str_tmp=str_tmp*line*"\n"
		end
	end
	# 问题: 没有了\n 
	# 可以去掉pattern2 后半部分,然后去掉空行
	# 开头的空格使用 lstrip
	#@info length(str_tmp)
	return str_tmp
end
function get_label_context(label,str4search)
	#	按照label名 提取内容
	# 所提取的标签内容包含label本身,例如:
	#  <h4>积分卡死了风景啊撒;哦地方</h4>
	
	tmp_str="<$label.+?</$label>"
	pattern=Regex(tmp_str)
	#@info "正则表达式的模式为:$(pattern)"
	result=[m.match for m=eachmatch(pattern,str4search)]
	return result
end
function 去标签(str,label="h4")
	#  使用replace函数 替换label为""(空串)
	#本来想用split,目前看来replace效果还行
	#
	
	pattern="<$label.*?>|</$label>"
	pattern=Regex(pattern)
	result=replace(str,pattern=>s"")
	#@info "$result \n $str "
	return result
end
function test_优化()
	str_tmp=html2txt("two.html")
	open("two.txt","w") do io
		write(io,str_tmp)
	end
return
	try
		INFO_URL="https://www.jin10.com/"
		文件名="jin10.html"
		#下载信息(INFO_URL,文件名)
		
		str_tmp=open(f->read(f, String), 文件名)
		str_vec=get_label_context("h4",str_tmp)
		data_vec=String[]
		for line in str_vec
			push!(data_vec,去标签(line))
		end
		数据归档(data_vec,"进10.txt")
	finally
		@info "执行结束"
	end
end
#test_优化()





