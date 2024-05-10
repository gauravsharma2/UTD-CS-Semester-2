Spark Streaming with Twitter and Kafka

How to run part 1:
1. We have to start the Kafka Environment
1.1 Go inside the kafka folder
1.2 Zookeeper: bin/zookeeper-server-start.sh config/zookeeper.properties
1.3 Kafka: bin/kafka-server-start.sh config/server.properties
1.4 Create a topic for the assignment: bin/kafka-topics.sh --create --topic assignment3part1 --bootstrap-server localhost:9092
1.5 Producer: bin/kafka-console-producer.sh --topic assignment3part1 --bootstrap-server localhost:9092
1.6 Consumer: bin/kafka-console-consumer.sh --topic assignment3part1 --from-beginning --bootstrap-server localhost:9092

2. We have start the ELK stack
2.1.1 Go to the directory of ElasticSearch
2.1.2 ./bin/elasticsearch

2.2.1 Go to the directory of Kibana
2.2.2 ./bin/kibana

2.3.1 Go to the directory of LogStash
2.3.2 ./bin/logstash

3. Python File
3.1 (optional) Update the search statement in the config file (config.ini)
3.2 python3 producer.py