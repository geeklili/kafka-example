## kafka_example
kafka配置样例
#### 1.下载Kafka和Zookeeper镜像文件
```
1，docker pull wurstmeister/kafka
2，docker pull wurstmeister/zookeeper
```
#### 2. 启动zookeeper容器
```
docker run -d --name zookeeper -p 2181:2181 -t wurstmeister/zookeeper
```
#### 3. 启动kafka容器
```
docker run  -d --name kafka \
-p 9092:9092 \
-e KAFKA_BROKER_ID=0 \ 
-e KAFKA_ZOOKEEPER_CONNECT=192.168.168.168:2181 \ 
-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://192.168.168.168:9092 \
-e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 -t wurstmeister/kafka 
```
这里面主要设置了4个参数
```
KAFKA_BROKER_ID=0               
KAFKA_ZOOKEEPER_CONNECT=192.168.168.168:2181
KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://192.168.168.168:9092
KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092
```
中间两个参数的192.168.168.168改为宿主机器的IP地址，如果不这么设置，可能会导致在别的机器上访问不到kafka。

#### 4. 测试kafka
进入kafka容器的命令行
```
docker exec -ti kafka /bin/bash
```
进入kafka所在目录
```
cd opt/kafka_2.12-1.1.0/
```

##### 4.1. 集群搭建(可选)
使用docker命令可快速在同一台机器搭建多个kafka，只需要改变brokerId和端口
```
docker run -d --name kafka1 \
-p 9093:9093 \
-e KAFKA_BROKER_ID=1 \
-e KAFKA_ZOOKEEPER_CONNECT=192.168.168.168:2181 \
-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://192.168.168.168:9093 \
-e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9093 -t wurstmeister/kafka
```
#### 5. 创建Replication为2，Partition为2的topic（如果没有集群，就都为1）
在kafka容器中的opt/kafka_2.12-1.1.0/目录下输入
```
bin/kafka-topics.sh --create --zookeeper 192.168.168.168:2181 --replication-factor 2 --partitions 2 --topic partopic
```
```
bin/kafka-topics.sh --create --zookeeper 192.168.168.168:2181 --replication-factor 1 --partitions 1 --topic partopic
```
#### 6. 查看topic的状态
在kafka容器中的opt/kafka_2.12-1.1.0/目录下输入
```
bin/kafka-topics.sh --describe --zookeeper 192.168.168.168:2181 --topic partopic
```
输出结果：
```
Topic:partopic  PartitionCount:2    ReplicationFactor:2 Configs:
    Topic: partopic Partition: 0    Leader: 0   Replicas: 0,1   Isr: 0,1
    Topic: partopic Partition: 1    Leader: 0   Replicas: 1,0   Isr: 0,1
```
显示每个分区的Leader机器为broker0，在broker0和1上具有备份，Isr代表存活的备份机器中存活的。 
当停掉kafka1后，
```
docker stop kafka1
```
再查看topic状态，输出结果：
```
Topic:partopic  PartitionCount:2    ReplicationFactor:2 Configs:
    Topic: partopic Partition: 0    Leader: 0   Replicas: 0,1   Isr: 0
    Topic: partopic Partition: 1    Leader: 0   Replicas: 1,0   Isr: 0
```