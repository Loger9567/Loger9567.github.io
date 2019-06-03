Elastic Search DSL
---

### 查询语句的结构
+ 一般的查询语句的结构
```shell
{
	QUERY_NAME: {
		ARGUMENT: VALUE,
		ARGUMENT: VALUE, ...
	}
}
```
+ 针对字段的查询语句的结构
```shell
{
    QUERY_NAME: {
        FIELD_NAME: {
            ARGUMENT: VALUE,
            ARGUMENT: VALUE,...
        }
    }
}
```


### _cat API
+ 查询当前集群的相关信息, 如: 集群index数量, 运行状态, 当前集群所在的ip
+ cat 
+ cat health 检查es集群运行状态 `curl -XGET "ip:9200/_cat/health?v"`
+ cat count 查询集群/index中的文档数量 
+ cat indices 查询当前集群中所有index的数据, 包括index的分片数, 文档数, 存储所用空间大小 `curl -XGET "ip:9200/_cat/indices?v"`



### Search API
+ query
	+ term  查询时判断文档是否包含某个具体的值, 不对查询条件做分词
	+ match 对查询条件分词, 然后用评分机制(TF/IDF)进行打分
	+ match_phrase 将查询条件作为一个整体短语严格查询
	+ bool 结合其他真值查询, 通常和 must, should, must_not一起组合出复杂的查询
	+ range 查询时指定某个字段在某个特定的范围
+ from 以一定的偏移量来查看检索结果, 默认从检索的第一条数据开始显示
+ size 指定检索结果中输出的条数, 默认为10条
+ sort 运行将检索结果以特定的字段进行排序显示
+ _source 指定检索结果输出的字段
+ script_fields 允许通过一个脚本来计算document中不存在的值
+ aggs 基于搜索查询, 可以嵌套聚合来组合复杂的需求

#### Query DSL
+ ES提供的一套完整的基于json格式的结构化查询方法, 包含2类不同的查询语义
	+ Leaf Query Clauses: 叶子查询句法指在指定的字段中搜索指定的值, 有match, term, range
	+ Compound Query Clauses: 复合查询句法会包含叶子查询句法和复合查询句法, 作用是为了多重查询, 有 bool , dis_max
	


### Query and Filter context
+ 查询语句的行为取决于它是查询型上下文还是过滤型上下文
+ Query Context: 这种上下文中, 返回的结果是: "结果和查询语句的匹配程度如何", 返回结果都会带上 _score
+ Filter Context: 这种上下文中, 查询语句表明匹配与否, ES内置式为这种上下文, 保留缓存来提高性能, 因此比Query Context快


### 具体用法
#### 查询所有 match_all
```shell
GET /_search    //所有索引，所有type下的所有数据都搜索出来
{
  "query": {
    "match_all": {}
  }
}
GET /test_index/_search    //指定一个index，搜索其下所有type的数据
{
  "query": {
    "match_all": {}
  }
}
GET /test_index,test_index2/_search    //同时搜索两个index下的数据
{
  "query": {
    "match_all": {}
  }
}
GET /*1,*2/_search    //按照通配符去匹配多个索引
{
  "query": {
    "match_all": {}
  }
}
GET /test_index/test_type/_search    //搜索一个index下指定的type的数据
{
  "query": {
    "match_all": {}
  }
}
GET /test_index/test_type,test_type2/_search    //可以搜索一个index下多个type的数据
{
  "query": {
    "match_all": {}
  }
}
GET /test_index,test_index2/test_type,test_type2/_search    //搜索多个index下的多个type的数据
{
  "query": {
    "match_all": {}
  }
}
GET /_all/test_type,test_type2/_search    //可以代表搜索所有index下的指定type的数据
{
  "query": {
    "match_all": {}
  }
}
```
#### 精确匹配
```shell
GET /_search
{
  "query": {
    "match": {
      "title": "elasticsearch"
    }
  }
}
```

#### 增删查改
+ 新增索引: 

```shell
PUT /lib/
{
  "settings": {
    "index":{
      "number_of_shards": 3,
      "number_of_replicas": 0
    }
  }
}
PUT lib2  # 新建索引lib2
GET/lib/_settings  # 查看配置
GET _all/settings  #查看所有
```

+ 新增文档

```shell
# 指定ID
PUT /lib/user/1
{
  "first_name": "Jane",
  "last_name": "Smith",
  "age": 36,
  "about": "I like ...",
  "intrests": ["music"]
}
# 使用ES默认ID
POST /lib/user
{
  "first_name": "Jane",
  "last_name": "Smith",
  "age": 36,
  "about": "I like ...",
  "intrests": ["music"]
}
GET /lib/user/1  #查询文档
GET /lib/user/1?_source=age,about  #查看指定字段
```
+ 更新文档

```shell
# 用一个新文档替换用PUT, _version会自增
PUT /lib/user/1
{
  "first_name": "Jane",
  "last_name": "Smith",
  "age": 30,
  "about": "I like ...",
  "intrests": ["music"]
}

# 直接更新指定字段, 如果字段与原来不同, 则_version会自增
POST /lib/user/1/_update
{
  "doc": {
    "age": 30
  }
}
```

+ 删除文档 `DELETE /lib/user/1` , `DELETE lib`

#### 批量获取文档 Multi Get API
```
# 获取所有字段
GET /_mget
{
  "docs": [
    {
      "_index": "lib",
      "_type": "user",
      "_id": 1
    },
    {
      "_index": "lib",
      "_type": "user",
      "_id": 2
    },
    {
      "_index": "lib",
      "_type": "user",
      "_id": 3
    }
  ]
}

# 获取指定字段
GET /_mget
{
  "docs": [
    {
      "_index": "lib",
      "_type": "user",
      "_id": 1,
      "_source": "intrests"
    },{
      "_index": "lib",
      "_type": "user",
      "_id": 1,
      "_source": ["age", "about"]
    }
  ]
}

# 获取相同索引下相同类型的文档
GET /lib/user/_mget
{
  "docs": [
    {
      "_id": 1
    },
    {
      "_id": 2
    }
  ]
}
# 或者
GET /lib/user/_mget
{
  "ids": [1,2]
}
GET /lib/user/_mget
{
  "ids": ["1","2"]
}
```

#### 批量操作 bulk
+ bulk的格式

```
{action: {metadata}}\n
{requestbody}\n
# action : 行为
#	create: 文档不存在时创建
#	update: 更新文档
#	index: 创建新文档或替换已有文档
#	delete: 删除一个文档
#	metadata: _index, _type, _id
#	create和index区别: 如果数据存在, create会失败, index会更新
# demo: {"delete" : {"_index": "lib", "_type":"user", "_id":1}}

# 批量添加
POST /lib2/books/_bulk
{"index":{"_id": 1}}
{"title":"java","price":55}
{"index":{"_id": 2}}
{"title":"HTML5","price":56}
{"index":{"_id": 3}}
{"title":"python","price":57}
{"index":{"_id": 4}}
{"title":"php","price":58}

# 批量混合操作, 最后一步的更新会报错
POST /lib2/books/_bulk
{"delete":{"_index":"lib2", "_type": "books", "_id":4}}
{"create":{"_index":"tt", "_type": "ttt", "_id":100}}
{"name":"lynn"}
{"index":{"_index":"tt", "_type": "ttt"}}
{"name": "zhangsan"}
{"update":{"_index":"lib2", "_type": "books", "_id":4}}
{"doc":{"price":54}}

```

#### 版本控制
```
# 默认使用内部版本, 乐观锁控制并发, 修改值后, 如果值与原来不同, _version自增1
PUT /lib/user/1
{
  "first_name": "AA",
  "last_name": "BB",
  "age": 30,
  "about": "I like ...",
  "intrests": ["code"]
}
# 指定当前版本号, 当version参数与_version值相等才会更新, 然后_version自增, 否则报错
PUT /lib/user/1?version=1
{
  "first_name": "AA",
  "last_name": "BB",
  "age": 30,
  "about": "I like ...",
  "intrests": ["code"]
}
# 使用外部版本, version必须大于_version才会更新, _version更新为 version, 否则报错
PUT /lib/user/1?version=2&version_type=external
{
  "first_name": "AA",
  "last_name": "BB",
  "age": 30,
  "about": "I like ...",
  "intrests": ["code"]
}
```




### 参考
> https://juejin.im/entry/5a580f2b6fb9a01c975a2bc4

> https://www.elastic.co/guide/cn/elasticsearch/guide/current/query-dsl-intro.html





