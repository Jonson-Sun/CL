
function word_get(filename)
	word_set=Set()
	for line in eachline(filename)
		union!(word_set,split(line))
	end
	
	@info "词,数量:$(length(word_set) )"
end

# 本文件的测试函数
function test()
	file_name="wordset.txt"
	word_get(file_name)
	
	sleep(10)
end
test()
