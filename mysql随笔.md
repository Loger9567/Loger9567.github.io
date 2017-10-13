# MySQL学习随笔

### 关于空值和 null 
+ [MySQL中NULL和空值的区别](http://blog.csdn.net/yu757371316/article/details/53033118)
+ [Mysql的空值与NULL的区别](http://www.cnblogs.com/apache-x/p/5386287.html)
+ null 不等于空值, null 对于不同的数据类型取值不一样, 对于 auto_increasement 的字段,会插入一个正整数序列; 对于timestamp 则插入的是当前日期, 如果是用空值的话会插入一个全0的日期.
+ 在使用 count 函数的时候会统计空值 '', 忽略 null

### 函数日期
+ [MySQL日期时间函数大全](http://www.cnblogs.com/zeroone/archive/2010/05/05/1727659.html)

### mysql中的各种连接
+ [mysql连接内连接、左连接、右连接、全连接](http://blog.csdn.net/miraclestar/article/details/6525246)


### 触发器
+ [数据库-触发器（定义、作用、使用方法、new/old虚拟表）](http://blog.csdn.net/zdplife/article/details/48155611)