Kafka和IBM MQ比较
---
### 1. Kafka
#### 基本概念
+ *broker* 部署了kafka实例的服务器节点
+ *topic* 区分不同类型的消息的主题, 一个broker上可以有同一个topic的多个partition.
+ *partition* 每个topic可以有一个或多个分区(<=broker数量),一般每个broker上会有多个分区
+ *replica* 保证集群HA的数据副本, 一般一个partition在一个broker上只会有一个replica
+ *producer* 生产者, 往kafka集群写数据
+ *consumer* 消费者, 从kafka集群读数据
+ *consumer group* 消费者组, 包含一个或多个消费者, 每个topic消息只能被消费者组中的某一个消费者消费


#### 什么是ISR?
+ 每个partition中的leader维护的与其基本保持同步的replica列表
+ 当ISR中所有replica都向leader发送ack后, leader才commit
+ 由于producer往kafka中发送数据可以是批量的, 当ISR中某个follower比leader消息落后太多, 或者超过一定时间没有发起数据复制请求, 则leader将其移出ISR, 差距缩小后可以动态添加进来.

```sh
//server配置
replica.lag.time.max.ms=10000
replica.lag.max.messages=4000
//topic配置
min.insync.replicas=1  //每个ISR中至少有多少个replica
//producer配置
request.required.acks=0
    //0相当于异步, 不需要leader回复, 立即返回;
    //1表示leader收到消息后发送ack, 丢了会重发, 丢的概率小
    //-1挡所有的follower都同步消息成功后发送ack,丢失的概率更小
```

#### replica恢复
+ partition中的leader挂了之后, kafka使用zookeeper从它的follower中选举一个leader, 并将挂掉的leader从ISR中移除
+ 当该leader后面重新启动之后, 它知道自己之前的数据到哪里了,尝试取它挂掉之后leader处理的数据, 完成后加入ISR


#### 消息的写入和同步
+ 每个partition有一个leader和多个follower(replica), producer只会往leader写,然后leader写到replica.
	+ 同步复制: 所有follower复制完成后才commit,然后应答生产者--一致性好, 高可用差
	+ 异步复制: leader拿到数据之后应答或不用应答生产者,等follower慢慢复制--高可用,一致性差
+ kafka采用的是follower pull模式
+ kafka只保证在同一个partition内部消息是有序的, 不同的partition间不保证
+ 使用偏移量来标识一条数据, 消费者可以改变偏移量来读取想要的数据





















### 3. 参考
> https://blog.csdn.net/qq_37502106/article/details/80271800
> https://www.jianshu.com/p/97011dab6c56