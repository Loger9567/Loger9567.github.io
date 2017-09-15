mysql 学习随笔
---

### 函数
#### found_rows()
+ 取出一张表的满足条件的记录的一部分(使用 limit), 同时也取出满足条件的记录的数量
	+ 先执行 `select sql_calc_found_rows * from crrs.advice where id>1 limit 5;`  获取满足条件的前5行.
	+ 再接着执行 `select found_rows() as fr; ` 得到满足条件的记录数.
