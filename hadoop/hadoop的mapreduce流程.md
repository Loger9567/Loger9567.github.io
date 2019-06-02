hadoop的mapreduce流程
---

### 简介
+ 一种分布式的计算方式, 指定一个map函数, 将一组键值对映射为一组新的键值对, 指定并发的reduce函数, 用来归约相同键的键值.
![mapreduce-pattern](resources/mapreduce-pattern.png)

### 基本流程
+ 读取文件 --> Map --> Reduce --> 写结果
![mapreduce-process-overview](resources/mapreduce-process-overview.png)
	+ combine  
		+ 分为map端和reduce端, 作用是将中间结果中相同key的kv对合并在一起, 便于减少网络传输, 可自定义, 默认不合并中间结果
		+ 通常map多,reduce少, 所以在reduce数据量大, 在map里面将数据归类, 这样到了reduce压力就轻了
		+ 例如: map为销售人员, reduce为销售经理, 如果销售人员不统计自己卖了多少件和多少钱, 那就需要销售经理统计, 为了减轻销售经理的压力, 那么这部分统计由 combine做就可以.
	+ partition
		+ 分割map每个节点的结果, 按照key分别映射给不同的reduce, 可以理解为归类, 默认使用hash, 可以自定义.
		+ 默认:  reducer = (key.hashCode() & Integer.MAX_VALUE) % numReduceTasks
		+ 这样可以将相同的key交给同一个reducer处理
	+ shuffle
		+ map端的shuffle
			+ spill溢写
				+ 每个map处理后的结果写入内存缓存区
				+ 对每一条kv进行分区
				+ 将相同分区的数据进行分区内排序
				+ 当内存缓存区写满后写入到磁盘
			+ merge合并: 将spill生成的小文件进行合并, 并排序
			+ 结束该map任务, 通知AM过来取数据
		+ reduce端的shuffle
			+ reduce启动多个线程, 通过网络到每台机器上拉取属于自己的数据
			+ merge合并: 
				+ 将每个map task中属于自己分区的数据进行合并
				+ 分区内排序
				+ 分组: 对相同key的value进行合并
		+ 优化
			+ combiner: 符合结合律 A+(B+C) == (A+B)+C
			+ compress: 减少磁盘IO和网络IO
				+ hadoop checknative: 可以检查压缩
				+ 替换lib/native可以修改本地压缩库, 常见压缩方式: snappy, lzo, lz4
				

### 详细流程
![mapreduce-process](resources/mapreduce-process.png)

### 多节点下的流程
![mapreduce-process-cluster](resources/mapreduce-process-cluster.png)

+ 通过InputFormat决定读取的数据的类型, 然后拆分成InputSplit, 每个InputSplit对应一个Map处理, InputFormat决定读取数据的格式, 可以是文件或数据库
+ InputSplit: 代表一个逻辑分片, 没有真正存储数据, 只提供一个如何将数据分片的方法, Split里面有Location信息, 利于数据局部化
+ RecordReader: 将InputSplit拆分为一个个kv对给Map处理
+ 大量小文件如何处理
	+ CombineFileInputFormat 可以将若干个Split打包成一个, 避免过多的Map任务
+ 如何计算split
	+ 通常一个split就是一个block
	+ 可通过 mapred.min.split.size, mapred.max.split.size, block.size来控制拆分大小
	+ 如果mapred.min.split.size大于block size, 则会将一个block拆分为多个split, 增加了Map任务数



### 引用
> https://www.w3cschool.cn/hadoop/flxy1hdd.html

> https://blog.csdn.net/bfqiwbifj/article/details/51352059