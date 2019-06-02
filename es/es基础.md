Elastic Search 基础
---

### Hive是什么
+ 数据仓库基础工具, 用于在Hadoop中处理结构化数据
+ 特点
	+ 存储架构在一个数据库中并处理数据到HDFS
	+ 用于OLAP, 而非OLTP
	+ 提供结构化查询语言 HiveQL(HQL)
	+ 广泛用途并且快速, 可扩展
+ 架构
![hive-arch](resources/hive-arch.jpg)


### 数据类型
+ 列类型
	+ 整型
		+ TINYINT    后缀Y,   i.e. 10Y
		+ SMALLINT  后缀S  i.e. 10S
		+ INT 无后缀  i.e. 10
		+ BIGINT 后缀 L  i.e. 10L
	+ 字符串类型: 恶意使用单引号或双引号指定
		+ VARCHAR  长度 1-65355
		+ CHAR   长度255
	+ 时间戳
		+ 支持传统的Unix时间戳, 可选纳秒精度
	+ 日期
	+ 浮点数
		+ `DECIMAL(precision, scale)`
	+ 联合类型: 异类数据的集合, 创建一个实例, 类似一个Map
		+ UNIONTYPE<int, double, array<string>, struct<a:int, b:string>>
		+ 示例
			+ `{0:1}` 
			+ `{1:2.0} `
			+ `{2:["three","four"]}` 
			+ `{3:{"a":5,"b":"five"}} `
			+ `{2:["six","seven"]} `
			+ `{3:{"a":8,"b":"eight"}} `
+ Null值:  NULL表示
+ 复杂类型
	+ 数组: ARRAY<data_type>
	+ 映射: MAP<primitive_type, data_type>
	+ 结构体: STRUCT<col_name : data_type [COMMENT col_comment], ...>


### HQL基本语法
+ 创建数据库 `CREATE DATABASE|SCHEMA [IF NOT EXISTS] <database name>`
+ 查看数据库列表: `SHOW DATABASES`
+ 删除数据库 `DROP DATABASE StatementDROP (DATABASE|SCHEMA) [IF EXISTS] database_name [RESTRICT|CASCADE];`
+ 建表
	
```shell
CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.] table_name
[(col_name data_type [COMMENT col_comment], ...)]
[COMMENT table_comment]
[ROW FORMAT row_format]
[STORED AS file_format]
```
+ 加载数据
	
```shell
LOAD DATA [LOCAL] INPATH 'filepath' [OVERWRITE] INTO TABLE tablename 
[PARTITION (partcol1=val1, partcol2=val2 ...)]
```
	
+ 修改表
	
```
ALTER TABLE name RENAME TO new_name
ALTER TABLE name ADD COLUMNS (col_spec[, col_spec ...])
ALTER TABLE name DROP [COLUMN] column_name
ALTER TABLE name CHANGE column_name new_name new_type
ALTER TABLE name REPLACE COLUMNS (col_spec[, col_spec ...])
```
+ 删除表 `DROP TABLE [IF EXISTS] table_name;`
+ 分区
	+ 新建分区
	
	```
	ALTER TABLE table_name ADD [IF NOT EXISTS] PARTITION partition_spec
[LOCATION 'location1'] partition_spec [LOCATION 'location2'] ...;
partition_spec:: (p_column = p_col_value, p_column = p_col_value, ...)
	```
	
	+ 重命名分区  

	```ALTER TABLE table_name PARTITION partition_spec RENAME TO PARTITION partition_spec```
	
	+ 删除分区
	
	```shell
	ALTER TABLE table_name DROP [IF EXISTS] PARTITION partition_spec, PARTITION partition_spec,...;
	
	```
+ 内置运算符
	+ 与一般的SQL没什么差别
	+ 多了 RLIKE, REGEXP 用于正则表达式匹配
+ 内置函数
	+ 与一般SQL没多少差别
+ 创建视图

	```
	CREATE VIEW [IF NOT EXISTS] view_name [(column_name [COMMENT column_comment], ...) ]
	[COMMENT table_comment]
	AS SELECT ...
	```

### 引用
> https://www.yiibai.com/hive/hive_data_types.html#article-start











