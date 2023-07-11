# banking-poc

## Apply docker compose

```
$ docker compose -f docker-compose-kafka.yml -f docker-compose-opensearch.yml -f docker-compose-zipkin.yml -f docker-compose.yml up -d
```
## Check all 12 containers
```
$ docker ps -a

IMAGE                                        PORTS              NAMES
tanminkwan/banking-miniagent                                    client-clyde
tanminkwan/banking-miniagent                                    client-bonnie
tanminkwan/banking-miniagent                                    client-john_dillinger
tanminkwan/banking-miniagent                                    banking-raffle
tanminkwan/banking-miniagent                 0.0.0.0:8382->5000 banking-deposit
tanminkwan/banking-miniagent                 0.0.0.0:8381->5000 banking-event
wurstmeister/zookeeper                       0.0.0.0:2181->2181 zookeeper
wurstmeister/kafka                           0.0.0.0:9092->9092 kafka
tanminkwan/cp-kafka-connect-added            0.0.0.0:8083->8083 banking-poc-kafka-connect-1
opensearchproject/opensearch                 0.0.0.0:9200->9200 opensearch
tanminkwan/opensearch-dashboards-no-security 0.0.0.0:5601->5601 opensearch-dashboards
openzipkin/zipkin                            0.0.0.0:9411->9411 zipkin
```
## Run kafka opensearch sink connector
```
echo '{"name":"opensearch-sink",
"config":{
"connector.class":"io.aiven.kafka.connect.opensearch.OpensearchSinkConnector",
"tasks.max":1,
"topics":"deposit.raffle",
"key.ignore":"true",
"connection.url":"http://172.17.0.1:9200",
"type.name":"log",
"schema.ignore":"true"
}
}'|curl -X POST -d @- http://localhost:8083/connectors --header "content-Type:application/json"
```